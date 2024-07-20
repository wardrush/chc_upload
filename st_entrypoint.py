import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import requests


# Function to generate a presigned URL
def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        st.error("AWS credentials not available")
        return None

    return response


# Streamlit app
def main(bucket_name):
    st.title("Upload File to S3")

    bucket_name = 'chc-ingestionbucket'
    object_name = st.text_input("Enter the S3 object name (e.g., 'uploads/file.txt'):")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None and object_name:
        # Generate presigned URL
        presigned_url = generate_presigned_url(bucket_name, object_name)

        if presigned_url:
            # Upload the file to S3 using the presigned URL
            files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.put(presigned_url, data=uploaded_file)

            if response.status_code == 200:
                st.success("File uploaded successfully")
            else:
                st.error(f"Failed to upload file. HTTP status code: {response.status_code}")


if __name__ == '__main__':
    main()
