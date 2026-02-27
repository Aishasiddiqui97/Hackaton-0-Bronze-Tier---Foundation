#!/usr/bin/env python3
"""
Instagram Business API MCP Server - Gold Tier
Provides Instagram media posting and analytics integration
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
LOG_PATH = Path("logs/instagram_actions.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [INSTAGRAM_SERVER] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class InstagramClient:
    """Instagram Graph API client with rate limiting and error handling."""

    def __init__(self, access_token: str, instagram_account_id: str):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_url = "https://graph.facebook.com/v19.0"
        self.rate_limit_remaining = 200

    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None, max_retries: int = 3) -> Dict[str, Any]:
        """Make API request with retry logic and rate limit handling."""
        params = params or {}
        params['access_token'] = self.access_token

        url = f"{self.base_url}/{endpoint}"

        for attempt in range(1, max_retries + 1):
            try:
                if method == 'GET':
                    response = requests.get(url, params=params, timeout=30)
                elif method == 'POST':
                    response = requests.post(url, params=params, json=data, timeout=30)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    logger.error(f"INSTAGRAM_RATE_LIMIT - Attempt {attempt}/{max_retries}")
                    time.sleep(60 * attempt)
                elif response.status_code == 190:
                    logger.error("INSTAGRAM_AUTH_ERROR - Access token expired")
                    raise
                else:
                    logger.error(f"INSTAGRAM_HTTP_ERROR - {e}")
                    if attempt == max_retries:
                        raise

            except requests.exceptions.RequestException as e:
                logger.error(f"INSTAGRAM_REQUEST_ERROR - Attempt {attempt}/{max_retries}: {str(e)}")
                if attempt == max_retries:
                    raise
                time.sleep(5 * attempt)

        return {}


class InstagramMCPServer:
    """MCP Server for Instagram Business operations."""

    def __init__(self, access_token: str, instagram_account_id: str):
        self.client = InstagramClient(access_token, instagram_account_id)
        self.instagram_account_id = instagram_account_id

    def post_instagram_media(self, image_url: str, caption: str, is_carousel: bool = False) -> Dict[str, Any]:
        """
        Post image to Instagram.

        Note: Instagram API requires a 2-step process:
        1. Create media container
        2. Publish the container
        """
        try:
            logger.info(f"INSTAGRAM_POST - Creating media: {caption[:50]}...")

            # Step 1: Create media container
            container_endpoint = f"{self.instagram_account_id}/media"
            container_params = {
                'image_url': image_url,
                'caption': caption
            }

            container_result = self.client._make_request('POST', container_endpoint, params=container_params)
            container_id = container_result.get('id')

            if not container_id:
                raise ValueError("Failed to create media container")

            logger.info(f"INSTAGRAM_CONTAINER - Created: {container_id}")

            # Step 2: Publish the container
            publish_endpoint = f"{self.instagram_account_id}/media_publish"
            publish_params = {'creation_id': container_id}

            publish_result = self.client._make_request('POST', publish_endpoint, params=publish_params)
            media_id = publish_result.get('id')

            logger.info(f"INSTAGRAM_SUCCESS - Media published: {media_id}")

            return {
                "success": True,
                "media_id": media_id,
                "container_id": container_id,
                "message": "Media published successfully"
            }

        except Exception as e:
            logger.error(f"INSTAGRAM_ERROR - post_instagram_media failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_instagram_metrics(self, media_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific Instagram post."""
        try:
            logger.info(f"INSTAGRAM_QUERY - Fetching metrics for media {media_id}")

            endpoint = f"{media_id}/insights"
            params = {
                'metric': 'engagement,impressions,reach,saved,likes,comments'
            }

            result = self.client._make_request('GET', endpoint, params=params)

            metrics = {}
            for item in result.get('data', []):
                metrics[item['name']] = item['values'][0]['value']

            # Get basic media data
            media_endpoint = f"{media_id}"
            media_params = {'fields': 'caption,timestamp,media_type,permalink'}
            media_data = self.client._make_request('GET', media_endpoint, params=media_params)

            logger.info(f"INSTAGRAM_SUCCESS - Metrics retrieved for {media_id}")

            return {
                "success": True,
                "media_id": media_id,
                "engagement": metrics.get('engagement', 0),
                "impressions": metrics.get('impressions', 0),
                "reach": metrics.get('reach', 0),
                "saved": metrics.get('saved', 0),
                "likes": metrics.get('likes', 0),
                "comments": metrics.get('comments', 0),
                "caption": media_data.get('caption', ''),
                "timestamp": media_data.get('timestamp'),
                "permalink": media_data.get('permalink')
            }

        except Exception as e:
            logger.error(f"INSTAGRAM_ERROR - get_instagram_metrics failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_account_insights(self, days: int = 7) -> Dict[str, Any]:
        """Get account-level insights for the past N days."""
        try:
            logger.info(f"INSTAGRAM_QUERY - Fetching account insights for {days} days")

            since = int((datetime.now() - timedelta(days=days)).timestamp())
            until = int(datetime.now().timestamp())

            endpoint = f"{self.instagram_account_id}/insights"
            params = {
                'metric': 'impressions,reach,profile_views,follower_count',
                'period': 'day',
                'since': since,
                'until': until
            }

            result = self.client._make_request('GET', endpoint, params=params)

            insights = {}
            for item in result.get('data', []):
                metric_name = item['name']
                values = item.get('values', [])

                if metric_name == 'follower_count':
                    # For follower_count, get the latest value
                    insights[metric_name] = values[-1].get('value', 0) if values else 0
                else:
                    # For other metrics, sum the values
                    total = sum(v.get('value', 0) for v in values)
                    insights[metric_name] = total

            logger.info(f"INSTAGRAM_SUCCESS - Account insights retrieved")

            return {
                "success": True,
                "period_days": days,
                "impressions": insights.get('impressions', 0),
                "reach": insights.get('reach', 0),
                "profile_views": insights.get('profile_views', 0),
                "follower_count": insights.get('follower_count', 0)
            }

        except Exception as e:
            logger.error(f"INSTAGRAM_ERROR - get_account_insights failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_weekly_instagram_summary(self) -> Dict[str, Any]:
        """Get comprehensive weekly summary for CEO Briefing."""
        try:
            logger.info("INSTAGRAM_QUERY - Generating weekly summary")

            # Get account insights
            insights = self.get_account_insights(days=7)

            if not insights['success']:
                return insights

            # Get recent media
            endpoint = f"{self.instagram_account_id}/media"
            params = {
                'fields': 'id,caption,timestamp,media_type',
                'limit': 10
            }
            media_result = self.client._make_request('GET', endpoint, params=params)

            media_list = media_result.get('data', [])

            # Get metrics for recent media
            media_metrics = []
            for media in media_list[:5]:  # Top 5 posts
                metrics = self.get_instagram_metrics(media['id'])
                if metrics['success']:
                    media_metrics.append({
                        'id': media['id'],
                        'caption': media.get('caption', '')[:100],
                        'engagement': metrics.get('engagement', 0),
                        'impressions': metrics.get('impressions', 0),
                        'likes': metrics.get('likes', 0),
                        'comments': metrics.get('comments', 0)
                    })

            # Find top performing post
            top_post = max(media_metrics, key=lambda x: x['engagement']) if media_metrics else None

            # Calculate engagement rate
            total_engagement = sum(m['engagement'] for m in media_metrics)
            total_impressions = sum(m['impressions'] for m in media_metrics)
            engagement_rate = round((total_engagement / max(total_impressions, 1)) * 100, 2)

            logger.info("INSTAGRAM_SUCCESS - Weekly summary generated")

            return {
                "success": True,
                "period": "7 days",
                "total_impressions": insights.get('impressions', 0),
                "total_reach": insights.get('reach', 0),
                "profile_views": insights.get('profile_views', 0),
                "follower_count": insights.get('follower_count', 0),
                "posts_published": len(media_list),
                "top_post": top_post,
                "engagement_rate": engagement_rate,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"INSTAGRAM_ERROR - get_weekly_instagram_summary failed: {str(e)}")
            return {"success": False, "error": str(e)}


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming MCP requests."""

    # Initialize server (credentials should come from .env in production)
    access_token = request.get('access_token', 'YOUR_ACCESS_TOKEN')
    instagram_account_id = request.get('instagram_account_id', 'YOUR_INSTAGRAM_ACCOUNT_ID')

    server = InstagramMCPServer(access_token, instagram_account_id)

    action = request.get('action')
    params = request.get('params', {})

    if action == 'post_instagram_media':
        return server.post_instagram_media(
            image_url=params.get('image_url'),
            caption=params.get('caption'),
            is_carousel=params.get('is_carousel', False)
        )

    elif action == 'get_instagram_metrics':
        return server.get_instagram_metrics(
            media_id=params.get('media_id')
        )

    elif action == 'get_account_insights':
        return server.get_account_insights(
            days=params.get('days', 7)
        )

    elif action == 'get_weekly_instagram_summary':
        return server.get_weekly_instagram_summary()

    else:
        return {"success": False, "error": f"Unknown action: {action}"}


def main():
    """MCP Server main loop."""
    logger.info("INSTAGRAM_SERVER_STARTED - Listening for MCP requests")

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
                logger.error(f"INSTAGRAM_SERVER_ERROR - {str(e)}")

    except KeyboardInterrupt:
        logger.info("INSTAGRAM_SERVER_STOPPED - User interrupt")


if __name__ == "__main__":
    main()
