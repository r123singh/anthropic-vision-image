import streamlit as st 
import anthropic
import base64
import httpx

API_KEY = st.secrets["API_KEY"]
client = anthropic.Anthropic(api_key = API_KEY)

def process_image(image_data, image_media_type):
    try:  
        message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type":"image",
                        "source":{
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data
                        }
                    }
                ]
            }
        ]
        )
        return message
    except Exception as e:
        return f"ERROR- Image does not match the media type"
    
def analyze_by_url(image_url):
    if "png" in image_url:
        image_media_type = "image/png"
    elif "jpeg" in image_url:
        image_media_type = "image/jpeg"
    elif "webp" in image_url:
        image_media_type = "image/webp"
    elif "gif" in image_url:
        image_media_type = "image/gif"
    else:
        return "INVALID_IMAGE_TYPE"
    image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")
    return process_image(image_data, image_media_type)

def analyze_by_file(img_file):
    img_type = img_file.name.split(".")[1]
    if img_type == "jpeg":
        image_media_type = "image/jpeg"
    elif img_type == "png":
        image_media_type = "image/png"
    elif img_type == "webp":
        image_media_type = "image/webp"
    elif img_type == "gif":
        image_media_type = "image/gif"
    else:
        return "INVALID_IMAGE_TYPE"
    image_data = base64.b64encode(img_file.read()).decode("utf-8")
    return process_image(image_data, image_media_type)

st.title("Anthropic Image Insights🤖👁️")

selected = st.sidebar.selectbox("Choose option", ["Image URL", "Image File"])
if selected == "Image URL":
    image_url = st.text_input("Image URL")
    if st.button("Analyze", use_container_width=True, type="primary"):
        st.image(image=image_url)
        response = analyze_by_url(image_url)
        if response == "INVALID_IMAGE_TYPE":
            st.info("Input image URL of types: jpeg, png, webp, gif")
        elif "ERROR" in response:
            st.error(response)
        else:
            st.write(f"### Analysis \n {response.content[0].text}")
        
elif selected == "Image File":
    image_file = st.file_uploader("Upload Image", type=["png", "jpeg", "webp", "gif"])
    if st.button("Analyze", use_container_width=True, type="primary"):
        st.image(image=image_file)
        response = analyze_by_file(image_file)
        if response == "INVALID_IMAGE_TYPE":
            st.info("Upload image with types: jpeg, png, webp, gif")
        elif "ERROR" in response:
            st.error(response)
        else:
            st.write(f"### Analysis \n {response.content[0].text}")


