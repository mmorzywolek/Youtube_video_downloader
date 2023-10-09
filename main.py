import streamlit as st
from pytube import YouTube

def main():
    if 'video_url' not in st.session_state:
        st.session_state.video_url = ''

    video_url = st.text_input("Enter YouTube Video URL", value=st.session_state.video_url)

    if st.button("Load Video"):
        st.session_state.video_url = video_url
        try:
            with st.spinner('Loading video...'):
                youtube = YouTube(video_url)
                video = youtube.streams.filter(progressive=True)

                video_list = []
                for i, stream in enumerate(video):
                    video_list.append(str(stream.resolution))

                st.session_state.video_list = video_list
                st.session_state.youtube = youtube

        except Exception as e:
            st.error(str(e))

    if 'video_list' in st.session_state:
        resolution = st.selectbox("Select Resolution", st.session_state.video_list)

        if st.button("Download Video"):
            video = st.session_state.youtube.streams.get_by_resolution(resolution)
            if video is None:
                st.error("This resolution is not available for the video.")
            else:
                with st.spinner('Preparing download link...'):
                    download_url = video.url
                    st.markdown(f'<a href="{download_url}" download>Click here</a>', unsafe_allow_html=True)
                    st.markdown('**Note:** If the video plays in your browser instead of downloading, right-click the video player and select "Save video as..." to download the video.')

if __name__ == '__main__':
    main()
