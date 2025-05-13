from loguru import logger
from openai import OpenAI

prompt = """
Anda adalah asisten ahli dalam menelusuri dokumen petunjuk teknis.
Untuk setiap pertanyaan dari pengguna, sarankan hingga lima pertanyaan tambahan yang relevan untuk membantu menemukan informasi yang dibutuhkan.
Setiap pertanyaan tambahan harus:
- Singkat dan langsung (tanpa kalimat majemuk)
- Hanya satu pertanyaan per baris (tanpa nomor atau tanda baca di depan)
- Beragam aspeknya, namun tetap berkaitan erat dengan pertanyaan awal
"""


class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        logger.info("OpenAI client initialized with API key {}".format(self.api_key))


class AugmentQueryGenerated:
    def __init__(self, api_key):
        self.openai = OpenAIClient(api_key=api_key)

    def augment(self, query, model="gpt-3.5-turbo") -> list[str]:
        """
        Augment the given query using OpenAI's API.
        """
        response = self.openai.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=150,
            temperature=0.7
        )
        augment_queries = response.choices[0].message.content.strip().split('\n')
        final_queries = [query] + augment_queries
        return final_queries
