#!/usr/bin/env python3
"""
Twitter (X) API v2 MCP Server - Gold Tier
Provides Twitter posting and analytics integration
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
LOG_PATH = Path("logs/twitter_actions.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [TWITTER_SERVER] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TwitterClient:
    """Twitter API v2 client with rate limiting and error handling."""

    def __init__(self, bearer_token: str, api_key: str = None, api_secret: str = None,
                 access_token: str = None, access_token_secret: str = None):
        self.bearer_token = bearer_token
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.base_url = "https://api.twitter.com/2"
        self.rate_limit_remaining = 300

    def _get_oauth_header(self) -> Dict[str, str]:
        """Get OAuth 1.0a header for write operations."""
        # For production, implement proper OAuth 1.0a signing
        # This is a simplified version
        return {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, params: Dict = None,
                     data: Dict = None, max_retries: int = 3) -> Dict[str, Any]:
        """Make API request with retry logic and rate limit handling."""
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_oauth_header()

        for attempt in range(1, max_retries + 1):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, params=params, timeout=30)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Update rate limit from headers
                if 'x-rate-limit-remaining' in response.headers:
                    self.rate_limit_remaining = int(response.headers['x-rate-limit-remaining'])

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    reset_time = int(response.headers.get('x-rate-limit-reset', 0))
                    wait_time = max(reset_time - int(time.time()), 60)
                    logger.error(f"TWITTER_RATE_LIMIT - Waiting {wait_time}s")
                    time.sleep(wait_time)
                elif response.status_code == 401:
                    logger.error("TWITTER_AUTH_ERROR - Invalid credentials")
                    raise
                else:
                    logger.error(f"TWITTER_HTTP_ERROR - {e}: {response.text}")
                    if attempt == max_retries:
                        raise

            except requests.exceptions.RequestException as e:
                logger.error(f"TWITTER_REQUEST_ERROR - Attempt {attempt}/{max_retries}: {str(e)}")
                if attempt == max_retries:
                    raise
                time.sleep(5 * attempt)

        return {}


class TwitterMCPServer:
    """MCP Server for Twitter operations."""

    def __init__(self, bearer_token: str, api_key: str = None, api_secret: str = None,
                 access_token: str = None, access_token_secret: str = None):
        self.client = TwitterClient(bearer_token, api_key, api_secret, access_token, access_token_secret)
        self.user_id = None

    def _get_user_id(self) -> str:
        """Get authenticated user's ID."""
        if self.user_id:
            return self.user_id

        try:
            result = self.client._make_request('GET', 'users/me')
            self.user_id = result.get('data', {}).get('id')
            return self.user_id
        except Exception as e:
            logger.error(f"TWITTER_ERROR - Failed to get user ID: {str(e)}")
            return None

    def post_tweet(self, content: str) -> Dict[str, Any]:
        """Post a single tweet."""
        try:
            logger.info(f"TWITTER_POST - Creating tweet: {content[:50]}...")

            if len(content) > 280:
                logger.warning(f"TWITTER_WARNING - Tweet exceeds 280 characters ({len(content)})")
                return {"success": False, "error": "Tweet exceeds 280 character limit"}

            data = {'text': content}

            result = self.client._make_request('POST', 'tweets', data=data)

            tweet_id = result.get('data', {}).get('id')

            logger.info(f"TWITTER_SUCCESS - Tweet posted: {tweet_id}")

            return {
                "success": True,
                "tweet_id": tweet_id,
                "text": content,
                "message": "Tweet posted successfully"
            }

        except Exception as e:
            logger.error(f"TWITTER_ERROR - post_tweet failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def post_thread(self, tweet_list: List[str]) -> Dict[str, Any]:
        """Post a thread of tweets."""
        try:
            logger.info(f"TWITTER_THREAD - Creating thread with {len(tweet_list)} tweets")

            tweet_ids = []
            reply_to_id = None

            for i, content in enumerate(tweet_list):
                if len(content) > 280:
                    logger.warning(f"TWITTER_WARNING - Tweet {i+1} exceeds 280 characters")
                    return {"success": False, "error": f"Tweet {i+1} exceeds 280 character limit"}

                data = {'text': content}

                if reply_to_id:
                    data['reply'] = {'in_reply_to_tweet_id': reply_to_id}

                result = self.client._make_request('POST', 'tweets', data=data)
                tweet_id = result.get('data', {}).get('id')

                if not tweet_id:
                    logger.error(f"TWITTER_ERROR - Failed to post tweet {i+1}")
                    return {"success": False, "error": f"Failed to post tweet {i+1}"}

                tweet_ids.append(tweet_id)
                reply_to_id = tweet_id

                # Small delay between tweets
                if i < len(tweet_list) - 1:
                    time.sleep(2)

            logger.info(f"TWITTER_SUCCESS - Thread posted: {len(tweet_ids)} tweets")

            return {
                "success": True,
                "tweet_ids": tweet_ids,
                "thread_length": len(tweet_ids),
                "message": "Thread posted successfully"
            }

        except Exception as e:
            logger.error(f"TWITTER_ERROR - post_thread failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_tweet_metrics(self, tweet_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific tweet."""
        try:
            logger.info(f"TWITTER_QUERY - Fetching metrics for tweet {tweet_id}")

            endpoint = f"tweets/{tweet_id}"
            params = {
                'tweet.fields': 'public_metrics,created_at,text',
                'expansions': 'author_id'
            }

            result = self.client._make_request('GET', endpoint, params=params)

            tweet_data = result.get('data', {})
            metrics = tweet_data.get('public_metrics', {})

            logger.info(f"TWITTER_SUCCESS - Metrics retrieved for {tweet_id}")

            return {
                "success": True,
                "tweet_id": tweet_id,
                "text": tweet_data.get('text', ''),
                "created_at": tweet_data.get('created_at'),
                "impressions": metrics.get('impression_count', 0),
                "likes": metrics.get('like_count', 0),
                "retweets": metrics.get('retweet_count', 0),
                "replies": metrics.get('reply_count', 0),
                "quotes": metrics.get('quote_count', 0),
                "engagement": metrics.get('like_count', 0) + metrics.get('retweet_count', 0) +
                             metrics.get('reply_count', 0) + metrics.get('quote_count', 0)
            }

        except Exception as e:
            logger.error(f"TWITTER_ERROR - get_tweet_metrics failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_user_tweets(self, max_results: int = 10) -> Dict[str, Any]:
        """Get recent tweets from authenticated user."""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return {"success": False, "error": "Failed to get user ID"}

            logger.info(f"TWITTER_QUERY - Fetching recent tweets for user {user_id}")

            endpoint = f"users/{user_id}/tweets"
            params = {
                'max_results': max_results,
                'tweet.fields': 'public_metrics,created_at'
            }

            result = self.client._make_request('GET', endpoint, params=params)

            tweets = result.get('data', [])

            logger.info(f"TWITTER_SUCCESS - Retrieved {len(tweets)} tweets")

            return {
                "success": True,
                "tweets": tweets,
                "count": len(tweets)
            }

        except Exception as e:
            logger.error(f"TWITTER_ERROR - get_user_tweets failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_weekly_twitter_summary(self) -> Dict[str, Any]:
        """Get comprehensive weekly summary for CEO Briefing."""
        try:
            logger.info("TWITTER_QUERY - Generating weekly summary")

            # Get recent tweets
            tweets_result = self.get_user_tweets(max_results=100)

            if not tweets_result['success']:
                return tweets_result

            tweets = tweets_result.get('tweets', [])

            # Filter tweets from last 7 days
            week_ago = datetime.now() - timedelta(days=7)
            recent_tweets = []

            for tweet in tweets:
                created_at = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                if created_at >= week_ago:
                    recent_tweets.append(tweet)

            # Calculate aggregate metrics
            total_impressions = 0
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            total_engagement = 0

            for tweet in recent_tweets:
                metrics = tweet.get('public_metrics', {})
                total_impressions += metrics.get('impression_count', 0)
                total_likes += metrics.get('like_count', 0)
                total_retweets += metrics.get('retweet_count', 0)
                total_replies += metrics.get('reply_count', 0)

            total_engagement = total_likes + total_retweets + total_replies

            # Find top performing tweet
            top_tweet = max(recent_tweets,
                          key=lambda t: t.get('public_metrics', {}).get('like_count', 0) +
                                       t.get('public_metrics', {}).get('retweet_count', 0)) if recent_tweets else None

            # Calculate engagement rate
            engagement_rate = round((total_engagement / max(total_impressions, 1)) * 100, 2)

            logger.info("TWITTER_SUCCESS - Weekly summary generated")

            return {
                "success": True,
                "period": "7 days",
                "tweets_posted": len(recent_tweets),
                "total_impressions": total_impressions,
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "total_engagement": total_engagement,
                "engagement_rate": engagement_rate,
                "top_tweet": {
                    "id": top_tweet.get('id'),
                    "text": top_tweet.get('text', '')[:100],
                    "likes": top_tweet.get('public_metrics', {}).get('like_count', 0),
                    "retweets": top_tweet.get('public_metrics', {}).get('retweet_count', 0)
                } if top_tweet else None,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"TWITTER_ERROR - get_weekly_twitter_summary failed: {str(e)}")
            return {"success": False, "error": str(e)}


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming MCP requests."""

    # Initialize server (credentials should come from .env in production)
    bearer_token = request.get('bearer_token', 'YOUR_BEARER_TOKEN')

    server = TwitterMCPServer(bearer_token)

    action = request.get('action')
    params = request.get('params', {})

    if action == 'post_tweet':
        return server.post_tweet(
            content=params.get('content')
        )

    elif action == 'post_thread':
        return server.post_thread(
            tweet_list=params.get('tweet_list', [])
        )

    elif action == 'get_tweet_metrics':
        return server.get_tweet_metrics(
            tweet_id=params.get('tweet_id')
        )

    elif action == 'get_weekly_twitter_summary':
        return server.get_weekly_twitter_summary()

    else:
        return {"success": False, "error": f"Unknown action: {action}"}


def main():
    """MCP Server main loop."""
    logger.info("TWITTER_SERVER_STARTED - Listening for MCP requests")

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
                logger.error(f"TWITTER_SERVER_ERROR - {str(e)}")

    except KeyboardInterrupt:
        logger.info("TWITTER_SERVER_STOPPED - User interrupt")


if __name__ == "__main__":
    main()
