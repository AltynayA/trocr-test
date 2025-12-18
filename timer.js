const start = Date.now();
await fetch('your_api_endpoint', { method: 'POST' });
const duration = Date.now() - start;
console.log(`Request took ${duration}ms`);
