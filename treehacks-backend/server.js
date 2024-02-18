const express = require('express');
const app = express();
const OpenAI = require('openai-api');

app.use(express.json()); // Middleware to parse JSON bodies

const OPENAI_API_KEY = 'your_openai_api_key_here'; // Replace with your actual OpenAI API key
const openai = new OpenAI(OPENAI_API_KEY);




app.post('/ask', async (req, res) => {
    const prompt = req.body.prompt;

    try {
        const gptResponse = await openai.createCompletion({
            engine: 'davinci', // You can use other engines as needed
            prompt: prompt,
            max_tokens: 150,
            temperature: 0.9,
        });

        res.json({ message: gptResponse.data.choices[0].text.trim() });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error communicating with OpenAI API' });
    }
});

const PORT = process.env.PORT || 5000; // Server port
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));