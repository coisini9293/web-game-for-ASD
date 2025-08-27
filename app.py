# streamlit run streamlit_demo.py
# Day 3: Streamlit frontend development and LangChain integration demo (with pagination)
import streamlit as st
import os
from multi_agent_framework import multi_agent_process

st.set_page_config(page_title="LangChain + Streamlit Agent Dialogue Demo", layout="centered")

st.title("LangChain + Streamlit Agent Dialogue Demo")

# Pagination: Dialogue, Mini Games, Camera Recording
# New pagination (Streamlit 1.10+)
tabs = st.tabs(["Dialogue", "Mini Game", "Camera Recording", "Tetris", "2048", "Sokoban"])

# For storing the latest generated HTML code
if 'latest_html' not in st.session_state:
    st.session_state['latest_html'] = None

# Globally disable page scrollbars to prevent arrow keys from scrolling the page
st.markdown("""
<style>
body, html {
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# Dialogue page
with tabs[0]:
    st.header("Multi-Agent Dialogue Area")
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Add prompt selection area
    st.subheader("🎯 Task Configuration")
    
    # By cognitive/functional goal (WHAT)
    st.write("**1. Cognitive/Functional Goal (WHAT)**")
    what_options = {
        "Perceptual Training": "Task Type: Auditory discrimination, visual tracking, tactile exploration; Functional Goal: Enhance sensory input processing ability; Game Example: Color block dragging",
        "Emotion Recognition and Regulation": "Task Type: Facial expression matching, emotion classification, self-emotion reporting; Functional Goal: Recognize others/self emotional states; Game Example: Simulated expression selection, emotion bar adjustment task",
        "Social Communication Skills": "Task Type: Turn-taking dialogue, greeting practice, virtual interaction; Functional Goal: Enhance understanding of social interaction rules; Game Example: NPC dialogue imitation practice",
        "Attention and Executive Function": "Task Type: Attention maintenance, working memory, multitasking; Functional Goal: Improve task completion and organizational ability; Game Example: Spot the difference, sorting game",
        "Interest-Guided Learning": "Task Type: Embed specific interest content in tasks; Functional Goal: Increase motivation, improve task acceptance; Game Example: Train number recognition, dinosaur matching"
    }
    selected_what = st.selectbox("Select Cognitive/Functional Goal:", list(what_options.keys()))
    
    # By interaction form (HOW)
    st.write("**2. Interaction Form (HOW)**")
    how_options = {
        "Gamified Task": "Task Feature: Emphasize rules, feedback, and scores; Game Example: Snake, 2048, matching game",
        "Story-based Task": "Task Feature: Scenario-driven, guide social reasoning; Game Example: 'Go shopping' interactive story",
        "Daily Simulation Task": "Task Feature: Simulate real-life scenarios; Game Example: Dressing, tooth brushing task guidance"
    }
    selected_how = st.selectbox("Select Interaction Form:", list(how_options.keys()))
    
    # By task difficulty and level (LEVEL)
    st.write("**3. Task Difficulty and Level (LEVEL)**")
    level_options = {
        "Low Difficulty": "Task Feature: Single modality, reactive, no social logic; Game Example: Click the appearing image",
        "Medium Difficulty": "Task Feature: Multimodal, with sequence/feedback rules; Game Example: Drag image to sequence position",
        "High Difficulty": "Task Feature: Intent reasoning, role-playing; Game Example: Choose the correct response in dialogue"
    }
    selected_level = st.selectbox("Select Task Difficulty:", list(level_options.keys()))
    
    # Show the combined full prompt
    prompt1 = what_options[selected_what]
    prompt2 = how_options[selected_how]
    prompt3 = level_options[selected_level]
    combined_prompt = f"{prompt1} | {prompt2} | {prompt3}"
    
    st.write("**📋 Full Prompt Preview:**")
    st.info(combined_prompt)
    
    # User input area
    st.subheader("💬 User Requirement")
    user_input = st.text_input("Please enter specific requirement:", placeholder="For example: I want a game about dinosaurs")
    
    # New: Normative prefix
    prompt_prefix = (
        "Please generate a high-quality H5 web mini-game with the following requirements:"
        "1. The game must have clear start and end buttons;"
        "2. The game must have basic functions such as scoring and replay;"
        "3. The game must disable arrow key scrolling of the webpage, and arrow keys are only for game operation;"
        "4. When the game ends, only a popup on the current page is allowed, and no popup when switching tabs."
        "Please strictly follow the above requirements."
    )
    
    # Combine all prompts
    full_prompt = f"{prompt_prefix} | Task Configuration: {combined_prompt} | User Requirement: {user_input}"
    
    if st.button("Send", key="chat_send"):
        progress = st.progress(0)
        st.info("Perception Agent running...")
        progress.progress(33)
        # --- New: Stepwise output from each Agent ---
        from multi_agent_framework import get_content
        from perception_agent import build_perception_agent
        from decision_agent import build_decision_agent
        from action_agent import build_action_agent, extract_html
        # Perception Agent
        perception_agent = build_perception_agent()
        type_result = perception_agent.invoke({"desc": full_prompt})
        type_str = get_content(type_result)
        st.info(f"Perception Agent: {type_str}")
        progress.progress(40)
        # Decision Agent
        decision_agent = build_decision_agent()
        decision = decision_agent.invoke({"type": type_str})
        decision_str = get_content(decision)
        st.info(f"Decision Agent: {decision_str}")
        progress.progress(60)
        # Action Agent - Always generate H5 game
        html_code = None
        st.info("Action Agent: Starting HTML generation...")
        action_agent = build_action_agent()
        html_code_raw = action_agent.invoke({"desc": full_prompt})
        
        # Debug: Show raw response info
        st.info(f"Action Agent: Raw response type: {type(html_code_raw)}")
        st.info(f"Action Agent: Raw response length: {len(str(html_code_raw))}")
        
        html_code = extract_html(html_code_raw)
        if html_code:
            st.info("Action Agent: HTML code generated successfully!")
            st.info(f"Action Agent: Extracted HTML length: {len(html_code)}")
            st.code(html_code[:500] + "..." if len(html_code) > 500 else html_code, language="html")
        else:
            st.warning("Action Agent: Failed to extract HTML code from response.")
            st.error("Action Agent: Raw response for debugging:")
            st.code(str(html_code_raw)[:1000] + "..." if len(str(html_code_raw)) > 1000 else str(html_code_raw), language="text")
        progress.progress(90)
        progress.progress(100)
        st.success("Multi-agent process completed!")
        # Save all Agent outputs to history
        st.session_state['history'].append({
            "user": user_input,
            "what": selected_what,
            "how": selected_how,
            "level": selected_level,
            "full_prompt": full_prompt,
            "type": type_str,
            "decision": decision_str,
            "html": html_code
        })
        # If there is html, save to session_state for mini game page
        if html_code:
            st.session_state['latest_html'] = html_code
            st.success("HTML code saved to session state!")
        else:
            st.warning("No HTML code to save.")
    
    # Show dialogue history
    st.markdown("### Dialogue History:")
    for item in st.session_state['history']:
        st.write(f"**You:** {item['user']}")
        st.write(f"**Task Configuration:** WHAT={item['what']}, HOW={item['how']}, LEVEL={item['level']}")
        st.write(f"**Full Prompt:** {item['full_prompt']}")
        st.write(f"**Perception Agent:** {item['type']}")
        st.write(f"**Decision Agent:** {item['decision']}")
        if item['html']:
            st.write("**[H5 Game HTML Snippet]**")
            st.code(item['html'], language="html")
        st.markdown("---")
    # Disable arrow key scrolling
    st.components.v1.html("""
    <script>
    document.addEventListener('keydown', function(e) {
        if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    """, height=0)

# Mini Game page
with tabs[1]:
    st.header("Web Mini Game Demo")
    st.info("H5 mini games can be embedded here, AI-generated supported.")
    
    # Add debug information
    st.write(f"**Debug: latest_html exists:** {st.session_state.get('latest_html') is not None}")
    if st.session_state.get('latest_html'):
        st.write(f"**Debug: latest_html length:** {len(st.session_state['latest_html'])}")
    
    # If there is the latest generated HTML, embed and display
    if st.session_state.get('latest_html'):
        st.success("Found HTML code! Displaying game...")
        st.components.v1.html(st.session_state['latest_html'], height=500)
    else:
        st.warning("No AI-generated H5 game HTML snippet yet. Please generate in the dialogue area for automatic display.")
    # Disable arrow key scrolling
    st.components.v1.html("""
    <script>
    document.addEventListener('keydown', function(e) {
                 if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    """, height=0)

# Camera Recording page
with tabs[2]:
    st.header("Camera Recording Agent (Local Save)")
    st.info("Click the button below to start recording. The video will be saved locally when you close the page or click stop.")
    html_code = """
    # Page structure
    <div>
      <video id='video' width='320' height='240' autoplay muted></video> #Show camera  
      <br>
      <button id='startBtn'>Start Recording</button> #Start recording
      <button id='stopBtn' disabled>Stop Recording</button> #Stop recording 
      <div id='progress' style='display:none;'>
        <p>Saving recording...</p> #Saving recording
        <progress id='saveProgress' value='0' max='100' style='width:320px;'></progress> #Progress bar  
      </div>
    </div>
    # Script
    <script>
    let mediaRecorder; #Create a MediaRecorder object
    let recordedChunks = []; #Create an empty array to store recorded video chunks
    let isRecording = false; #Boolean to track recording status
    const video = document.getElementById('video'); #Get video element
    const startBtn = document.getElementById('startBtn'); #Get start button element
    const stopBtn = document.getElementById('stopBtn'); #Get stop button element
    const progressDiv = document.getElementById('progress'); #Get progress bar element
    const saveProgress = document.getElementById('saveProgress'); #Get progress bar element
    navigator.mediaDevices.getUserMedia({ video: true, audio: true }) #Get camera and microphone permission
      .then(stream => {
        video.srcObject = stream; #Set video stream as video element source
        startBtn.onclick = () => {
          recordedChunks = []; #Create an empty array to store recorded video chunks
          mediaRecorder = new MediaRecorder(stream); #Create a MediaRecorder object
          mediaRecorder.ondataavailable = e => {
            if (e.data.size > 0) recordedChunks.push(e.data); #If recorded video chunk size > 0, add to recordedChunks array
          };
          mediaRecorder.onstop = saveVideo; #Call saveVideo function when recording stops
          mediaRecorder.start(); #Start recording
          isRecording = true; #Set recording status to true
          startBtn.disabled = true; #Disable start button
          stopBtn.disabled = false; #Enable stop button
        };
        stopBtn.onclick = () => {
          if (mediaRecorder && isRecording) {
            mediaRecorder.stop(); #Stop recording
            isRecording = false; #Set recording status to false
            startBtn.disabled = false; #Enable start button
            stopBtn.disabled = true; #Disable stop button
          }
        };
        window.addEventListener('beforeunload', function (e) {
          if (isRecording) {
            mediaRecorder.stop(); #Stop recording
            isRecording = false; #Set recording status to false
            startBtn.disabled = false; #Enable start button
            stopBtn.disabled = true; #Disable stop button
            progressDiv.style.display = 'block'; #Show progress bar
            saveProgress.value = 0; #Set progress bar value to 0
          }
        });
      });
    function saveVideo() {
      progressDiv.style.display = 'block'; #Show progress bar
      saveProgress.value = 10; #Set progress bar value to 10
      setTimeout(() => {
        saveProgress.value = 50; #Set progress bar value to 50
        const blob = new Blob(recordedChunks, { type: 'video/webm' }); #Create a Blob object
        const url = URL.createObjectURL(blob); #Create a URL object
        const a = document.createElement('a'); #Create an a element
        a.style.display = 'none'; #Hide a element
        a.href = url; #Set href attribute of a element
        a.download = 'recorded_video.webm'; #Set download attribute of a element
        document.body.appendChild(a); #Add a element to body
        a.click(); #Click a element
        setTimeout(() => {
          document.body.removeChild(a); #Remove a element
          window.URL.revokeObjectURL(url); #Release URL object
          saveProgress.value = 100; #Set progress bar value to 100  
          setTimeout(() => {
            progressDiv.style.display = 'none'; #Hide progress bar
            alert('Recording has been saved locally!'); #Prompt recording saved
          }, 500);
        }, 1000);
      }, 1000);
    }
    </script>
    """
    st.components.v1.html(html_code, height=400)
    # Disable arrow key scrolling
    st.components.v1.html("""
    <script>
    document.addEventListener('keydown', function(e) {
        if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    """, height=0)

    # New: Attention detection function
    st.header("Attention Detection (WebSocket Real-time Feedback)")
    st.info("This page will detect your attention status in real time. If distracted, a popup will appear. Please allow camera permission. Click the button below to start detection.")
    attention_html = '''
    <div>
      <video id="attention_video" width="320" height="240" autoplay muted style="border:1px solid #aaa;"></video>
      <canvas id="attention_canvas" width="320" height="240" style="display:none;"></canvas>
      <br>
      <button id="start_attention_btn">Start Detection</button>
    </div>
    <script>
    let ws_attention = null;
    let warned_attention = false;
    let attention_stream = null;
    let attention_timer = null;
    function connectWSAttention() {
      ws_attention = new WebSocket('ws://localhost:8765/attention');
      ws_attention.onopen = function() {
        console.log('WebSocket for attention connected');
      };
      ws_attention.onmessage = function(event) {
        let data = JSON.parse(event.data);
        if(data.status === 'distracted' && !warned_attention) {
          warned_attention = true;
          alert('Attention not focused, please focus on the screen!');
          setTimeout(()=>{warned_attention=false;}, 3000); // No repeated popup within 3 seconds
        }
      };
      ws_attention.onclose = function() {
        setTimeout(connectWSAttention, 1000); // Reconnect on disconnect
      };
    }
    document.getElementById('start_attention_btn').onclick = function() {
      if (ws_attention && ws_attention.readyState === 1) return;
      connectWSAttention();
      const attention_video = document.getElementById('attention_video');
      const attention_canvas = document.getElementById('attention_canvas');
      const attention_ctx = attention_canvas.getContext('2d');
      navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        attention_video.srcObject = stream;
        attention_stream = stream;
        if (attention_timer) clearInterval(attention_timer);
        attention_timer = setInterval(() => {
          attention_ctx.drawImage(attention_video, 0, 0, attention_canvas.width, attention_canvas.height);
          let dataURL = attention_canvas.toDataURL('image/jpeg');
          if(ws_attention && ws_attention.readyState === 1) {
            ws_attention.send(JSON.stringify({ image: dataURL }));
          }
        }, 200); // 5fps
      });
    }
    </script>
    '''
    st.components.v1.html(attention_html, height=300)

# Tetris page
with tabs[3]:
    st.header("Tetris")
    st.info("Classic Tetris game, use arrow keys to move.")
    tetris_html = '''
    <iframe src="https://www.xarg.org/project/tetris/" style="width:100vw;height:100vh;border:none;" frameborder="0" scrolling="no"></iframe>
    <script>
    document.addEventListener('keydown', function(e) {
        if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    '''
    st.components.v1.html(tetris_html, height=1000)

# 2048 page
with tabs[4]:
    st.header("2048 Puzzle Game")
    st.info("2048 merge number game, use arrow keys to move.")
    game2048_html = '''
    <iframe src="https://2048game.com/" width="400" height="600" frameborder="0" scrolling="no"></iframe>
    <script>
    document.addEventListener('keydown', function(e) {
        if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    '''
    st.components.v1.html(game2048_html, height=620)

# Sokoban page
with tabs[5]:
    st.header("Sokoban")
    st.info("Classic Sokoban puzzle game, use arrow keys to move.")
   
    sokoban_html = '''
    <iframe src="https://kippenjungle.nl/COI/sokoban.html" style="width:100vw;height:95vh;min-height:600px;border:none;display:block;margin:0 auto;" frameborder="0" scrolling="no"></iframe>
    <script>
    document.addEventListener('keydown', function(e) {
        if([37,38,39,40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);
    </script>
    '''
    st.components.v1.html(sokoban_html, height=1000)

