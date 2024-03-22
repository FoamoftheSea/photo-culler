import ollama

system_message = '''
You are an expert in grading photographs based on quality. Photographers depend on your masterfully calculated quality 
scores to narrow down the images that they need to review after large shoots, saving them many hours of manual effort.
'''

system_message = system_message.replace("\n", " ")
model_file = f'''
FROM llava
SYSTEM {system_message}
'''

ollama.create(model='llava:photo-culler', modelfile=model_file)
