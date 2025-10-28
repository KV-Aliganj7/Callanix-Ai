// config.js - API Configuration
const CONFIG = {
  MODELS: [
    { 
      id: 'model_1', 
      apiKey: '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', 
      model: 'meta-llama/llama-4-scout:free', 
      endpoint: 'https://openrouter.ai/api/v1/chat/completions', 
      requestCount: 0, 
      maxRequestsPerMinute: 60 
    },
    { 
      id: 'model_2', 
      apiKey: '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', 
      model: 'meta-llama/llama-4-scout:free', 
      endpoint: 'https://openrouter.ai/api/v1/chat/completions', 
      requestCount: 0, 
      maxRequestsPerMinute: 60 
    },
    { 
      id: 'model_3', 
      apiKey: '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', 
      model: 'meta-llama/llama-4-scout:free', 
      endpoint: 'https://openrouter.ai/api/v1/chat/completions', 
      requestCount: 0, 
      maxRequestsPerMinute: 60 
    },
    { 
      id: 'model_4', 
      apiKey: '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', 
      model: 'meta-llama/llama-4-scout:free', 
      endpoint: 'https://openrouter.ai/api/v1/chat/completions', 
      requestCount: 0, 
      maxRequestsPerMinute: 60 
    },
    { 
      id: 'model_5', 
      apiKey: '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', 
      model: 'meta-llama/llama-4-scout:free', 
      endpoint: 'https://openrouter.ai/api/v1/chat/completions', 
      requestCount: 0, 
      maxRequestsPerMinute: 60 
    }
  ],
  USER_LIMIT: 13000,
  SYSTEM_PROMPT: `You are Callanix, an expert AI assistant for students. Your goal is to provide clear, accurate, and easy-to-read answers formatted in clean HTML. You MUST use the following tags: <h1>, <h2>, <h3>, <p>, <strong>, <em>, <u>, <ul>, <ol>, <li>, <table>, <tr>, <th>, <td>, <hr>, <blockquote>, <code>, <pre>, <sub>, <sup>, and <div class="formula"> for math. Do NOT use Markdown.`
};