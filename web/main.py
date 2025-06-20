import time

import requests
import streamlit as st


class Config:
    BACKEND_URL = "https://api-chat.robbypambudi.com"
    PAGE_TITLE = "Informatics Chatbot"
    BACKGROUND_COLOR = "#F0F2F6"
    PRIMARY_COLOR = "#2C3E50"  # warna teks untuk user
    ASSISTANT_COLOR = "#34495E"  # warna teks untuk assistant


class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }


class ChatBotApp:
    def __init__(self):
        st.set_page_config(
            page_title=Config.PAGE_TITLE,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.collection_name = None
        self.collection_description = None
        self.collection_id = None
        self._apply_custom_css()
        self._init_session_state()

    def _init_session_state(self):
        self.user_id = 'test_development'
        if "chat_histories" not in st.session_state:
            st.session_state.chat_histories = {}

        if self.user_id not in st.session_state["chat_histories"]:
            default_msg = ChatMessage(
                role="assistant",
                content="👋 Selamat datang di chatbot kami! Silakan pilih koleksi untuk memulai."
            )
            st.session_state["chat_histories"][self.user_id] = [
                default_msg.to_dict()
            ]

    def _apply_custom_css(self):
        pass

    def _render_sidebar(self):
        with st.sidebar:
            st.title("💬 Selamat Datang!")
            st.write(
                "Sebuah chatbot yang dirancang untuk membantu Anda menjawab pertanyaan dengan cepat dan akurat.")
            # Author

            st.markdown("---")
            st.write("🔍 Silakan pilih koleksi yang ingin Anda gunakan untuk bertanya.")

            data = requests.get(
                f"{Config.BACKEND_URL}/api/v1/collection?ordering=&page_size=10&page=1&collection_name=&id")
            if data.status_code == 200:
                collections = data.json()
                if collections['status'] == 'success':
                    collections = collections['data']
                    collection_names = [{
                        "id": collection['id'],
                        "name": collection['collection_name'],
                        "description": collection['description']
                    }
                        for collection in collections
                    ]

                    selected_collection = st.selectbox(
                        "📚 Pilih Koleksi",
                        options=[collection['name'] for collection in collection_names],
                        format_func=lambda x: x
                    )
                    if selected_collection:
                        for collection in collection_names:
                            if collection['name'] == selected_collection:
                                self.collection_name = collection['name']
                                self.collection_description = collection['description']
                                self.collection_id = collection['id']
                                break
            else:
                st.error("❌ Gagal mengambil data koleksi.")

            st.markdown("---")
            st.write(
                "Dibuat untuk mendapatkan gelar teknik informatika di [Institut Teknologi Sepuluh Nopember Surabaya](https://www.its.ac.id/)")
            st.write("👨‍🎓 Robby Pambudi - TC21")
            # Github

    def _append_message(self, role: str, content: str):
        st.session_state["chat_histories"][self.user_id].append({
            "role": role,
            "content": content
        })

    def display_messages(self, role: str, content):
        with st.chat_message(role):
            st.markdown(content, unsafe_allow_html=True)

    def _handle_input(self):
        user_input = st.chat_input("💭 Tanyakan sesuatu...")
        if not user_input:
            return
        if not self.collection_name:
            st.error("⚠️ Mohon pilih koleksi terlebih dahulu.")
            return
        self._append_message("user", user_input)
        self.display_messages("user", user_input)
        self._send_and_receive(user_input)
        print(f"Chat history: {st.session_state['chat_histories'][self.user_id]}")

    def display_chat_history(self):
        for message in st.session_state["chat_histories"][self.user_id]:
            self.display_messages(message["role"], message["content"])

    def _send_and_receive(self, user_input):
        full_response = ""

        with st.chat_message("assistant"):
            placeholder = st.empty()

            # Tampilkan efek 'Assistant sedang mengetik...'
            typing_text = "🟡 Asisten sedang mengetik"
            for i in range(3):
                placeholder.markdown(typing_text + "." * (i + 1))
                time.sleep(0.3)
            try:
                response = requests.post(
                    f"{Config.BACKEND_URL}/api/v1/questions/stream",
                    data={
                        "question_id": f"{self.user_id}_{self.collection_id}_{int(time.time())}",
                        "question_text": user_input,
                        "collection_id": self.collection_id,
                        "using_augment_query": True,
                    },
                    stream=True,
                    timeout=60,
                )

                response.raise_for_status()

                for chunk in response.iter_lines():
                    if chunk:
                        text = chunk.decode("utf-8").removeprefix("data: ")
                        full_response += text
                        placeholder.markdown(
                            full_response,
                            unsafe_allow_html=True,
                        )

                if not full_response:
                    full_response = "⚠️ Tidak ada jawaban dari server."
                    placeholder.markdown(full_response, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Gagal menghubungi server: {e}")
                print(f"Error: {e}")
                return

            self._append_message("assistant", full_response)

    def run(self):
        self._render_sidebar()
        if self.collection_name and self.collection_description:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(to right, #2980B9, #6DD5ED);
                    padding: 16px 24px;
                    border-radius: 12px;
                    color: white;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                ">
                    <h3 style="margin-bottom: 5px;">📂 Koleksi Aktif: <span style="color: #F9E79F;">{self.collection_name}</span></h3>
                    <p style="margin: 0; font-size: 15px;">{self.collection_description}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                    <div style="
                        background-color: #FDEDEC;
                        padding: 16px;
                        border-left: 5px solid #E74C3C;
                        border-radius: 8px;
                        color: #C0392B;
                        font-weight: 500;
                    ">
                        ⚠️ <strong>Belum ada koleksi yang dipilih.</strong> Silakan pilih koleksi terlebih dahulu untuk memulai chat.
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)

        self.display_chat_history()
        self._handle_input()


if __name__ == "__main__":
    app = ChatBotApp()
    app.run()
