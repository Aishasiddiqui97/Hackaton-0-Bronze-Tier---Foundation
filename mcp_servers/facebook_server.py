#!/usr/bin/env python3
"""
Facebook Business API MCP Server - Gold Tier
Provides Facebook page posting and analytics integration
"""

import json
import logging
import sys
import requests
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

# Logging setup
LOG_PATH = Path("logs/facebook_actions.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [FACEBOOK_SERVER] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class FacebookClient:
    """Facebook Graph API client with rate limiting and error handling."""

    def __init__(self, access_token: str, page_id: str):
        self.access_token = access_token
        self.page_id = page_id
        self.base_url = "https://graph.facebook.com/v19.0"
        self.rate_limit_remaining = 200
        self.rate_limit_reset = None

    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None, max_retries: int = 3) -> Dict[str, Any]:
        """Make API request with retry logic and rate limit handling."""
        params = params or {}
        params['access_token'] = self.access_token

        url = f"{self.base_url}/{endpoint}"

        for attempt in range(1, max_retries + 1):
            try:
                # Check rate limit
                if self.rate_limit_remaining < 10:
                    if self.rate_limit_reset and datetime.now() < self.rate_limit_reset:
                        wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
                        logger.warning(f"FACEBOOK_RATE_LIMIT - Waiting {wait_time}s")
                        time.sleep(wait_time)

                if method == 'GET':
                    response = requests.get(url, params=params, timeout=30)
                elif method == 'POST':
                    response = requests.post(url, params=params, json=data, timeout=30)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Update rate limit info from headers
                if 'X-Business-Use-Case-Usage' in response.headers:
                    usage = json.loads(response.headers['X-Business-Use-Case-Usage'])
                    self.rate_limit_remaining = 200 - usage.get('call_count', 0)

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limit
                    logger.error(f"FACEBOOK_RATE_LIMIT - Attempt {attempt}/{max_retries}")
                    time.sleep(60 * attempt)  # Exponential backoff
                elif response.status_code == 190:  # Token expired
                    logger.error("FACEBOOK_AUTH_ERROR - Access token expired")
                    raise
                else:
                    logger.error(f"FACEBOOK_HTTP_ERROR - {e}")
                    if attempt == max_retries:
                        raise

            except requests.exceptions.RequestException as e:
                logger.error(f"FACEBOOK_REQUEST_ERROR - Attempt {attempt}/{max_retries}: {str(e)}")
                if attempt == max_retries:
                    raise
                time.sleep(5 * attempt)

        return {}


class FacebookMCPServer:
    """MCP Server for Facebook Business operations."""

    def __init__(self, access_token: str, page_id: str):
        self.client = FacebookClient(access_token, page_id)
        self.page_id = page_id

    def post_to_facebook(self, content: str, link: str = None, image_url: str = None) -> Dict[str, Any]:
        """Post content to Facebook page."""
        try:
            logger.info(f"FACEBOOK_POST - Creating post: {content[:50]}...")

            data = {'message': content}

            if link:
                data['link'] = link

            if image_url:
                data['url'] = image_url
                endpoint = f"{self.page_id}/photos"
            else:
                endpoint = f"{self.page_id}/feed"

            result = self.client._make_request('POST', endpoint, data=data)

            post_id = result.get('id', result.get('post_id'))

            logger.info(f"FACEBOOK_SUCCESS - Post created: {post_id}")

            return {
                "success": True,
                "post_id": post_id,
                "message": "Post published successfully"
            }

        except Exception as e:
            logger.error(f"FACEBOOK_ERROR - post_to_facebook failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_post_metrics(self, post_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific post."""
        try:
            logger.info(f"FACEBOOK_QUERY - Fetching metrics for post {post_id}")

            # Get post insights
            endpoint = f"{post_id}/insights"
            params = {
                'metric': 'post_impressions,post_engaged_users,post_reactions_by_type_total'
            }

            result = self.client._make_request('GET', endpoint, params=params)

            metrics = {}
            for item in result.get('data', []):
                metrics[item['name']] = item['values'][0]['value']

            # Get basic post data
            post_endpoint = f"{post_id}"
            post_params = {'fields': 'message,created_time,shares'}
            post_data = self.client._make_request('GET', post_endpoint, params=post_params)

            logger.info(f"FACEBOOK_SUCCESS - Metrics retrieved for {post_id}")

            return {
                "success": True,
                "post_id": post_id,
                "impressions": metrics.get('post_impressions', 0),
                "engaged_users": metrics.get('post_engaged_users', 0),
                "reactions": metrics.get('post_reactions_by_type_total', {}),
                "shares": post_data.get('shares', {}).get('count', 0),
                "created_time": post_data.get('created_time')
            }

        except Exception as e:
            logger.error(f"FACEBOOK_ERROR - get_post_metrics failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_page_insights(self, days: int = 7) -> Dict[str, Any]:
        """Get page-level insights for the past N days."""
        try:
            logger.info(f"FACEBOOK_QUERY - Fetching page insights for {days} days")

            since = int((datetime.now() - timedelta(days=days)).timestamp())
            until = int(datetime.now().timestamp())

            endpoint = f"{self.page_id}/insights"
            params = {
                'metric': 'page_impressions,page_engaged_users,page_fans,page_post_engagements',
                'period': 'day',
                'since': since,
                'until': until
            }

            result = self.client._make_request('GET', endpoint, params=params)

            insights = {}
            for item in result.get('data', []):
                metric_name = item['name']
                values = item.get('values', [])
                total = sum(v.get('value', 0) for v in values)
                insights[metric_name] = total

            logger.info(f"FACEBOOK_SUCCESS - Page insights retrieved")

            return {
                "success": True,
                "period_days": days,
                "impressions": insights.get('page_impressions', 0),
                "engaged_users": insights.get('page_engaged_users', 0),
                "new_fans": insights.get('page_fans', 0),
                "post_engagements": insights.get('page_post_engagements', 0)
            }

        except Exception as e:
            logger.error(f"FACEBOOK_ERROR - get_page_insights failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_weekly_facebook_summary(self) -> Dict[str, Any]:
        """Get comprehensive weekly summary for CEO Briefing."""
        try:
            logger.info("FACEBOOK_QUERY - Generating weekly summary")

            # Get page insights
            insights = self.get_page_insights(days=7)

            if not insights['success']:
                return insights

            # Get recent posts
            endpoint = f"{self.page_id}/posts"
            params = {
                'fields': 'id,message,created_time',
                'limit': 10
            }
            posts_result = self.client._make_request('GET', endpoint, params=params)

            posts = posts_result.get('data', [])

            # Get metrics for recent posts
            post_metrics = []
            for post in posts[:5]:  # Top 5 posts
                metrics = self.get_post_metrics(post['id'])
                if metrics['success']:
                    post_metrics.append({
                        'id': post['id'],
                        'message': post.get('message', '')[:100],
                        'impressions': metrics.get('impressions', 0),
                        'engaged_users': metrics.get('engaged_users', 0)
                    })

            # Find top performing post
            top_post = max(post_metrics, key=lambda x: x['engaged_users']) if post_metrics else None

            logger.info("FACEBOOK_SUCCESS - Weekly summary generated")

            return {
                "success": True,
                "period": "7 days",
                "total_impressions": insights.get('impressions', 0),
                "total_engaged_users": insights.get('engaged_users', 0),
                "new_followers": insights.get('new_fans', 0),
                "posts_published": len(posts),
                "top_post": top_post,
                "engagement_rate": round(insights.get('engaged_users', 0) / max(insights.get('impressions', 1), 1) * 100, 2),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"FACEBOOK_ERROR - get_weekly_facebook_summary failed: {str(e)}")
            return {"success": False, "error": str(e)}


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming MCP requests."""

    # Initialize server (credentials should come from .env in production)
    access_token = request.get('access_token', 'YOUR_ACCESS_TOKEN')
    page_id = request.get('page_id', 'YOUR_PAGE_ID')

    server = FacebookMCPServer(access_token, page_id)

    action = request.get('action')
    params = request.get('params', {})

    if action == 'post_to_facebook':
        return server.post_to_facebook(
            content=params.get('content'),
            link=params.get('link'),
            image_url=params.get('image_url')
        )

    elif action == 'get_post_metrics':
        return server.get_post_metrics(
            post_id=params.get('post_id')
        )

    elif action == 'get_page_insights':
        return server.get_page_insights(
            days=params.get('days', 7)
        )

    elif action == 'get_weekly_facebook_summary':
        return server.get_weekly_facebook_summary()

    else:
        return {"success": False, "error": f"Unknown action: {action}"}


def main():
    """MCP Server main loop."""
    logger.info("FACEBOOK_SERVER_STARTED - Listening for MCP requests")

    try:
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = handle_mcp_request(request)
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                error_response = {"success": False, "error": f"Invalid JSON: {str(e)}"}
                print(json.dumps(error_response), flush=True)

            except Exception as e:
                error_response = {"success": False, "error": f"Server error: {str(e)}"}
                print(json.dumps(error_response), flush=True)
                logger.error(f"FACEBOOK_SERVER_ERROR - {str(e)}")

    except KeyboardInterrupt:
        logger.info("FACEBOOK_SERVER_STOPPED - User interrupt")


if __name__ == "__main__":
    main()
