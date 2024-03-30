async function generateResponse() {
    const inputText = document.getElementById('customer-tweet').value;
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_text: inputText }),
    });

    if (!response.ok) {
        alert('Failed to generate response');
        return;
    }

    const data = await response.json();

    var similarTweetContent = `Customer's tweet: ${data.similar_customer_tweet}\n\nCompany's tweet: ${data.similar_company_tweet}`;

    document.getElementById('generated-response').value = data.response;
    document.getElementById('similar-tweet').value = similarTweetContent;
}