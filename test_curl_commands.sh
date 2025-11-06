#!/bin/bash
# Test pagination and filtering with curl commands

BASE_URL="http://127.0.0.1:8000"

echo "🧪 Testing Smart Study Buddy API Pagination & Filtering"
echo "======================================================="

# Test basic pagination
echo -e "\n📄 Basic Notes List:"
curl -s "$BASE_URL/api/notes/" | jq '.count, .current_page, .total_pages, (.results | length)'

# Test pagination with page size
echo -e "\n📄 Page 1 with 5 items:"
curl -s "$BASE_URL/api/notes/?page=1&page_size=5" | jq '.current_page, .page_size, (.results | length)'

# Test search
echo -e "\n🔍 Search for 'python':"
curl -s "$BASE_URL/api/notes/?search=python" | jq '.count, (.results | length)'

# Test filtering
echo -e "\n🔧 Filter notes with summaries:"
curl -s "$BASE_URL/api/notes/?has_summary=true" | jq '.count'

# Test sorting
echo -e "\n📊 Sort by title (ascending):"
curl -s "$BASE_URL/api/notes/?ordering=title" | jq '.results[0].title // "No results"'

# Test combined filters
echo -e "\n🎯 Combined: search + filter + sort:"
curl -s "$BASE_URL/api/notes/?search=test&has_summary=true&ordering=-created_at&page_size=3" | jq '.count, .page_size'

# Test quizzes
echo -e "\n🧠 Quizzes List:"
curl -s "$BASE_URL/api/quizzes/" | jq '.count // "No quizzes"'

# Test quiz attempts
echo -e "\n📈 Quiz Attempts:"
curl -s "$BASE_URL/api/quiz/attempts/" | jq '.count // "No attempts"'

echo -e "\n✅ Testing complete!"
echo "📖 Check Swagger docs at: $BASE_URL/api/docs/"