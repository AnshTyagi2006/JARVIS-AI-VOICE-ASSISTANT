from ddgs import DDGS


class WebService:
    """Provides free web-search capabilities for JARVIS."""

    SPORTS_KEYWORDS = [
        "score",
        "runs",
        "wicket",
        "match",
        "cricket",
        "football",
        "soccer",
        "basketball",
        "tennis",
        "player",
        "innings",
    ]

    NEWS_KEYWORDS = [
        "latest news",
        "news",
        "headlines",
        "today",
        "recent",
        "latest update",
    ]

    def search(self, query, max_results=5):
        """Search the web for a query."""

        if not query:
            return []

        try:
            results = DDGS().text(
                query,
                region="in-en",
                safesearch="moderate",
                max_results=max_results,
            )

            return list(results)

        except Exception as error:
            print(f"Web search error: {error}")
            return []

    def search_news(self, query, max_results=5):
        """Search specifically for news."""

        if not query:
            return []

        try:
            results = DDGS().news(
                query,
                region="in-en",
                safesearch="moderate",
                max_results=max_results,
            )

            return list(results)

        except Exception as error:
            print(f"News search error: {error}")
            return []

    def get_answer(self, query):
        """Search the web and return the most relevant result."""

        if not query:
            return None

        query_lower = query.lower()

        if self._is_news_query(query_lower):
            results = self.search_news(
                query,
                max_results=5,
            )

        elif self._is_sports_query(query_lower):
            results = []

            for sports_query in self._build_sports_queries(query):
                search_results = self.search(
                    sports_query,
                    max_results=5,
                )

                results.extend(search_results)

            results = self._remove_duplicate_results(results)

        else:
            results = self.search(
                query,
                max_results=5,
            )

        if not results:
            return None

        return self._select_best_result(
            results,
            query_lower,
        )

    @classmethod
    def _is_sports_query(cls, query):
        """Detect sports-related questions."""

        return any(
            keyword in query
            for keyword in cls.SPORTS_KEYWORDS
        )

    @classmethod
    def _is_news_query(cls, query):
        """Detect news-related questions."""

        return any(
            keyword in query
            for keyword in cls.NEWS_KEYWORDS
        )

    @staticmethod 
    def _build_sports_queries(query):
        """Build targeted searches for sports questions."""

        return [
            f'"{query}" cricket',
            f'{query} score runs innings',
            f'{query} latest match scorecard',
            f'{query} ESPNcricinfo',
            f'{query} Cricbuzz scorecard',
        ]

    @staticmethod
    def _select_best_result(results, query):
        """Select the most relevant search result."""

        query_words = {
            word.strip(".,?!")
            for word in query.split()
            if len(word) > 2
        }

        best_result = None
        best_score = -1

        blocked_terms = [
            "homepage",
            "live cricket score",
            "cricket home",
            "sports home",
            "cricket schedule",
        ]

        for result in results:
            title = result.get("title", "").lower()
            body = result.get("body", "").lower()

            text = f"{title} {body}"

            # Reject generic portal/homepage results.
            if any(term in text for term in blocked_terms):
                continue

            score = 0

            # Query keyword relevance.
            for word in query_words:
                if word in title:
                    score += 3
                elif word in body:
                    score += 1

            # Strong signals for actual score information.
            score_terms = [
                "runs",
                "score",
                "scored",
                "innings",
                "balls",
                "batting",
                "scorecard",
            ]

            for term in score_terms:
                if term in text:
                    score += 2

            # Prefer actual scorecard/result pages.
            if "scorecard" in text:
                score += 5

            if score > best_score:
                best_score = score
                best_result = result

        if best_result is None:
            best_result = results[0]

        return {
            "title": best_result.get("title", ""),
            "body": best_result.get("body", ""),
            "url": (
                best_result.get("href")
                or best_result.get("url")
                or ""
            ),
        }
        
    @staticmethod
    def _remove_duplicate_results(results):
        """Remove duplicate search results."""

        unique = []
        seen_urls = set()

        for result in results:
            url = (
                result.get("href")
                or result.get("url")
                or ""
            )

            if url and url in seen_urls:
                continue

            if url:
                seen_urls.add(url)

            unique.append(result)

        return unique   