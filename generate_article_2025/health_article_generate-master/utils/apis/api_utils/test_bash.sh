curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 5e0402a3-7673-415b-a0a5-09e51bdfc560" \
  -d '{
    "model": "ep-20250225110519-6hpgz",
    "messages": [
      {"role": "system","content": "你是人工智能助手."},
      {"role": "user","content": "请详细介绍下你自己。"}
    ]
  }