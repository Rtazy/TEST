import openai

def generate_post(prompt):
    # Set your OpenAI API key
    api_key = "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"
    openai.api_key = api_key

    # Specify the model and parameters
    model = "text-davinci-002"  # You can use other models provided by OpenAI

    # Generate the post using OpenAI API
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=200  # You can adjust the max_tokens parameter based on your needs
    )

    # Extract the generated text from the response
    generated_post = response['choices'][0]['text']

    return generated_post

# Example usage
prompt_text = "Create engaging and informative social media posts for Al Nour Foundation, focusing on empowering and integrating people with special needs into society. Generate content that highlights the foundation's mission, achievements, and upcoming events. Consider including personal stories of beneficiaries, success stories, and calls to action for donations or volunteer participation. Ensure the posts are inclusive, respectful, and inspire community support. Emphasize the importance of creating an inclusive society and showcase the positive impact of the foundation's work. You may also integrate relevant hashtags and visuals to enhance the posts' reach and appeal"
generated_post = generate_post(prompt_text)
print(generated_post)
