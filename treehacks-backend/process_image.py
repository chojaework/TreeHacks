import gradio as gr

def process_image(image):
    # 이미지 처리 로직 구현
    return f"Processed image: {image.name}"

iface = gr.Interface(fn=process_image, inputs=gr.inputs.Image(), outputs="text")

if __name__ == "__main__":
    iface.launch()
