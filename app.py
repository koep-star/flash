import streamlit as st
import json
import os
from datetime import datetime, timedelta
import random
from PIL import Image
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Flashcard App",
    page_icon="🎯",
    layout="wide"
)

class FlashcardApp:
    def __init__(self):
        self.data_file = "flashcards.json"
        self.progress_file = "progress.json"
        self.load_data()
        self.load_progress()
    
    def load_data(self):
        """Load flashcard data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.flashcards = json.load(f)
        else:
            self.flashcards = []
    
    def save_data(self):
        """Save flashcard data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.flashcards, f, indent=2, ensure_ascii=False)
    
    def load_progress(self):
        """Load user progress and suppression data"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            self.progress = {}
    
    def save_progress(self):
        """Save user progress and suppression data"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_available_cards(self):
        """Get cards that are not currently suppressed"""
        current_time = datetime.now()
        available_cards = []
        
        for i, card in enumerate(self.flashcards):
            card_id = str(i)
            if card_id in self.progress:
                suppress_until = datetime.fromisoformat(self.progress[card_id].get('suppress_until', '1900-01-01'))
                if current_time >= suppress_until:
                    available_cards.append((i, card))
            else:
                available_cards.append((i, card))
        
        return available_cards
    
    def suppress_card(self, card_index, days):
        """Suppress a card for a specified number of days"""
        card_id = str(card_index)
        suppress_until = datetime.now() + timedelta(days=days)
        
        if card_id not in self.progress:
            self.progress[card_id] = {}
        
        self.progress[card_id]['suppress_until'] = suppress_until.isoformat()
        self.progress[card_id]['last_reviewed'] = datetime.now().isoformat()
        self.save_progress()

def main():
    st.title("🎯 Flashcard Learning App")
    
    # Initialize app
    if 'app' not in st.session_state:
        st.session_state.app = FlashcardApp()
    
    app = st.session_state.app
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Study", "Manage Cards", "Statistics"])
    
    if page == "Study":
        study_page(app)
    elif page == "Manage Cards":
        manage_cards_page(app)
    elif page == "Statistics":
        statistics_page(app)

def study_page(app):
    st.header("📚 Study Session")
    
    available_cards = app.get_available_cards()
    
    if not available_cards:
        st.warning("No cards available for study! All cards might be suppressed or you haven't added any cards yet.")
        return
    
    st.info(f"Available cards: {len(available_cards)} out of {len(app.flashcards)} total")
    
    # Initialize session state for current card
    if 'current_card_index' not in st.session_state:
        st.session_state.current_card_index = 0
        st.session_state.show_answer = False
        st.session_state.available_indices = [idx for idx, _ in available_cards]
        random.shuffle(st.session_state.available_indices)
    
    # Get current card
    if st.session_state.current_card_index < len(st.session_state.available_indices):
        card_idx = st.session_state.available_indices[st.session_state.current_card_index]
        current_card = app.flashcards[card_idx]
        
        # Display card counter
        st.write(f"Card {st.session_state.current_card_index + 1} of {len(st.session_state.available_indices)}")
        
        # Display question
        st.subheader("Question:")
        st.write(current_card['question'])
        
        # Display image if present
        if 'image' in current_card and current_card['image']:
            if os.path.exists(current_card['image']):
                try:
                    image = Image.open(current_card['image'])
                    st.image(image, caption="Question Image", max_width=400)
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            else:
                st.warning(f"Image file not found: {current_card['image']}")
        
        # Reveal answer button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔍 Reveal Answer", key="reveal"):
                st.session_state.show_answer = True
        
        # Show answer if revealed
        if st.session_state.show_answer:
            st.subheader("Answer:")
            st.success(current_card['answer'])
            
            # Difficulty buttons
            st.subheader("How well did you know this?")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("😰 Hard (1 day)", key="hard"):
                    app.suppress_card(card_idx, 1)
                    next_card()
            
            with col2:
                if st.button("🤔 Medium (3 days)", key="medium"):
                    app.suppress_card(card_idx, 3)
                    next_card()
            
            with col3:
                if st.button("😊 Easy (7 days)", key="easy"):
                    app.suppress_card(card_idx, 7)
                    next_card()
            
            with col4:
                if st.button("🎯 Perfect (14 days)", key="perfect"):
                    app.suppress_card(card_idx, 14)
                    next_card()
        
        # Skip card option
        if st.button("⏭️ Skip Card", key="skip"):
            next_card()
    
    else:
        st.success("🎉 You've completed all available cards!")
        if st.button("🔄 Start Over"):
            reset_study_session()

def next_card():
    """Move to next card"""
    st.session_state.current_card_index += 1
    st.session_state.show_answer = False
    st.rerun()

def reset_study_session():
    """Reset study session"""
    st.session_state.current_card_index = 0
    st.session_state.show_answer = False
    if 'available_indices' in st.session_state:
        random.shuffle(st.session_state.available_indices)
    st.rerun()

def manage_cards_page(app):
    st.header("📝 Manage Cards")
    
    tab1, tab2, tab3 = st.tabs(["Add New Card", "View All Cards", "Import Cards"])
    
    with tab1:
        st.subheader("Add New Flashcard")
        
        with st.form("add_card_form"):
            question = st.text_area("Question:", height=100)
            answer = st.text_area("Answer:", height=100)
            
            # Image upload
            uploaded_file = st.file_uploader("Upload an image (optional)", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("Add Card"):
                if question and answer:
                    new_card = {
                        "question": question,
                        "answer": answer
                    }
                    
                    # Handle image upload
                    if uploaded_file:
                        # Create images directory if it doesn't exist
                        os.makedirs("images", exist_ok=True)
                        
                        # Save uploaded file
                        image_path = f"images/{len(app.flashcards)}_{uploaded_file.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        new_card["image"] = image_path
                    
                    app.flashcards.append(new_card)
                    app.save_data()
                    st.success("Card added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in both question and answer!")
    
    with tab2:
        st.subheader("All Flashcards")
        
        if app.flashcards:
            for i, card in enumerate(app.flashcards):
                with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
                    st.write("**Question:**", card['question'])
                    st.write("**Answer:**", card['answer'])
                    
                    if 'image' in card and card['image']:
                        if os.path.exists(card['image']):
                            try:
                                image = Image.open(card['image'])
                                st.image(image, caption="Card Image", max_width=200)
                            except Exception as e:
                                st.error(f"Error loading image: {e}")
                    
                    # Show suppression status
                    card_id = str(i)
                    if card_id in app.progress:
                        suppress_until = datetime.fromisoformat(app.progress[card_id].get('suppress_until', '1900-01-01'))
                        if datetime.now() < suppress_until:
                            st.warning(f"Suppressed until: {suppress_until.strftime('%Y-%m-%d %H:%M')}")
                    
                    if st.button(f"Delete Card {i+1}", key=f"delete_{i}"):
                        app.flashcards.pop(i)
                        app.save_data()
                        st.rerun()
        else:
            st.info("No cards available. Add some cards to get started!")
    
    with tab3:
        st.subheader("Import Cards from CSV")
        st.write("Upload a CSV file with columns: 'question', 'answer', 'image' (optional)")
        
        uploaded_csv = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_csv:
            try:
                df = pd.read_csv(uploaded_csv)
                
                if 'question' in df.columns and 'answer' in df.columns:
                    st.write("Preview:")
                    st.dataframe(df.head())
                    
                    if st.button("Import Cards"):
                        for _, row in df.iterrows():
                            new_card = {
                                "question": str(row['question']),
                                "answer": str(row['answer'])
                            }
                            
                            if 'image' in df.columns and pd.notna(row['image']):
                                new_card["image"] = str(row['image'])
                            
                            app.flashcards.append(new_card)
                        
                        app.save_data()
                        st.success(f"Imported {len(df)} cards successfully!")
                        st.rerun()
                else:
                    st.error("CSV must contain 'question' and 'answer' columns!")
            
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

def statistics_page(app):
    st.header("📊 Statistics")
    
    if not app.flashcards:
        st.info("No cards available for statistics.")
        return
    
    # Basic statistics
    total_cards = len(app.flashcards)
    available_cards = len(app.get_available_cards())
    suppressed_cards = total_cards - available_cards
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cards", total_cards)
    
    with col2:
        st.metric("Available Cards", available_cards)
    
    with col3:
        st.metric("Suppressed Cards", suppressed_cards)
    
    # Suppression details
    if app.progress:
        st.subheader("Card Status Details")
        
        current_time = datetime.now()
        status_data = []
        
        for i, card in enumerate(app.flashcards):
            card_id = str(i)
            status = "Available"
            next_review = "Now"
            
            if card_id in app.progress:
                suppress_until = datetime.fromisoformat(app.progress[card_id].get('suppress_until', '1900-01-01'))
                if current_time < suppress_until:
                    status = "Suppressed"
                    next_review = suppress_until.strftime('%Y-%m-%d %H:%M')
            
            status_data.append({
                "Card": i + 1,
                "Question": card['question'][:50] + "..." if len(card['question']) > 50 else card['question'],
                "Status": status,
                "Next Review": next_review
            })
        
        df = pd.DataFrame(status_data)
        st.dataframe(df, use_container_width=True)
    
    # Reset progress option
    st.subheader("⚠️ Reset Progress")
    st.write("This will clear all suppression data and make all cards available for study.")
    
    if st.button("Reset All Progress", type="secondary"):
        app.progress = {}
        app.save_progress()
        st.success("Progress reset successfully!")
        st.rerun()

if __name__ == "__main__":
    main()
