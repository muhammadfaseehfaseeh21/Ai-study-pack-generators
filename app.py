# app.py
import streamlit as st
import json
from workflow import StudyPackOrchestrator

st.set_page_config(page_title="Multi-Stage AI Study Pack Generator", page_icon="🎓", layout="wide")

st.title("🎓 Multi-Stage AI Study Pack Generator")
st.caption("Structured multi-stage AI pipeline for generating personalized study materials.")

# Sidebar Configuration
with st.sidebar:
    st.header("🔑 Authentication")
    api_key = st.text_input("Gemini API Key", type="password")
    st.markdown("[Get Gemini API Key](https://aistudio.google.com/)")
    
    st.divider()
    st.header("⚙️ Workflow Options")
    enable_review = st.checkbox("Enable Quality Audit & Refinement", value=True)
    max_retries = st.slider("Max Refinement Retries", 1, 3, 2)

notes_input = st.text_area("Paste your study notes or raw lecture text:", height=220, placeholder="Paste material here...")

if st.button("Generate Study Pack", type="primary"):
    if not api_key:
        st.error("Please enter a Gemini API Key in the sidebar.")
    elif not notes_input.strip():
        st.warning("Please enter study material to process.")
    else:
        orchestrator = StudyPackOrchestrator(api_key=api_key)
        status_box = st.status("Executing Multi-Stage Pipeline...", expanded=True)
        
        try:
            # STAGE 1: Planning
            status_box.write("🧠 **Stage 1: Planning** — Extracting key concepts & difficulty...")
            plan = orchestrator.run_stage_planning(notes_input)
            
            # STAGE 2: Content Generation
            status_box.write("📝 **Stage 2: Content Generation** — Writing summary & flashcards...")
            content = orchestrator.run_stage_content(notes_input, plan)
            
            # STAGE 3: Assessment
            status_box.write("🎯 **Stage 3: Assessment** — Constructing 4-option quiz...")
            assessment = orchestrator.run_stage_assessment(notes_input, plan)
            
            # STAGE 4 & 5: Audit & Refinement
            if enable_review:
                status_box.write("🔍 **Stage 4: Quality Audit** — Validating content accuracy...")
                audit = orchestrator.run_stage_audit(notes_input, content, assessment)
                
                retries = 0
                while not audit.passed and retries < max_retries:
                    retries += 1
                    status_box.write(f"🔄 **Stage 5: Refinement (Attempt {retries})** — {audit.feedback}")
                    content = orchestrator.run_stage_refinement(notes_input, audit.feedback)
                    audit = orchestrator.run_stage_audit(notes_input, content, assessment)

            status_box.update(label="Workflow Complete!", state="complete", expanded=False)
            
            # --- RENDER RESULTS ---
            st.success(f"Study Pack Ready! Assessed Difficulty: **{plan.target_difficulty}**")
            
            tab_summary, tab_cards, tab_quiz, tab_export = st.tabs(["📖 Summary", "🎴 Flashcards", "📝 Quiz", "💾 Export"])
            
            with tab_summary:
                st.markdown(content.summary)
                
            with tab_cards:
                c1, c2 = st.columns(2)
                for idx, card in enumerate(content.flashcards):
                    target_col = c1 if idx % 2 == 0 else c2
                    with target_col:
                        with st.expander(f"📌 {card.concept}: {card.question}"):
                            st.write(f"**Answer:** {card.answer}")
                            
            with tab_quiz:
                for idx, q in enumerate(assessment.quiz, 1):
                    st.markdown(f"**{idx}. {q.question}**")
                    choice = st.radio(f"Select answer for Q{idx}:", q.options, key=f"q_{idx}", label_visibility="collapsed")
                    if st.button(f"Submit Answer #{idx}", key=f"btn_{idx}"):
                        if choice == q.correct_answer:
                            st.success("Correct!")
                        else:
                            st.error(f"Incorrect. Correct answer: {q.correct_answer}")
                        st.info(f"**Explanation:** {q.explanation}")
                    st.divider()

            with tab_export:
                export_payload = {
                    "difficulty": plan.target_difficulty,
                    "summary": content.summary,
                    "flashcards": [f.model_dump() for f in content.flashcards],
                    "quiz": [q.model_dump() for q in assessment.quiz]
                }
                st.download_button(
                    label="Download Study Pack (.JSON)",
                    data=json.dumps(export_payload, indent=2),
                    file_name="study_pack.json",
                    mime="application/json"
                )

        except Exception as e:
            status_box.update(label="Pipeline Failed", state="error")
            st.error(f"Error encountered: {str(e)}")
