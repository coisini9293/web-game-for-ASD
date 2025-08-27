---
title: ASD Multi-Agent Web Game
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
tags:
- streamlit
- ai
- healthcare
- autism
pinned: false
short_description: Multi-agent system for autism children
---
# ASD Multi-Agent Web Game

## Project Introduction

This is an agent-assisted system designed specifically for children with autism, providing personalized interactive experiences for children with autism through a multi-agent framework combined with eye-tracking technology.

## Project Architecture

### Core Components

1. **Multi-Agent Framework** (`multi_agent_framework.py`)

   - Coordinates perception, decision, and action agents
   - Processes user input and generates responses
2. **Perception Agent** (`perception_agent.py`)

   - Analyzes user input and context
   - Extracts key information and emotional states
3. **Decision Agent** (`decision_agent.py`)

   - Makes decisions based on perception results
   - Selects the most suitable interaction strategy
4. **Action Agent** (`action_agent.py`)

   - Executes decisions and generates responses
   - Creates HTML content and interactive elements
5. **Eye-Tracking Module** (`gaze_tracking/`)

   - Real-time eye movement tracking
   - Provides attention analysis functionality
6. **Web Interface** (`app.py`)

   - Streamlit-based user interface
   - Provides intuitive interactive experience

## Features

### Main Features

- **Intelligent Dialogue**: Multi-turn dialogue system based on LangChain
- **Eye Tracking**: Real-time monitoring of user attention status
- **Personalized Response**: Adjusts interaction strategies based on user status
- **Web Interface**: User-friendly interface design

### Technical Features

- **Multi-Agent Collaboration**: Three-layer architecture of perception-decision-action
- **Real-time Processing**: Supports real-time eye movement data analysis and response
- **Scalability**: Modular design for easy feature expansion

## Installation and Usage

### Requirements

- Python 3.8+
- Camera device (for eye tracking)
- Stable internet connection

### Deployment Methods

#### Method 1: Hugging Face Spaces (Recommended)

1. **Access Application**: Directly visit [Hugging Face Spaces Link]
2. **No Installation Required**: Application is already running in the cloud, ready to use
3. **Environment Variables**: Configure `OPENAI_API_KEY` in Spaces settings

#### Method 2: Local Deployment

1. **Clone Project**

   ```bash
   git clone [project address]
   cd ASD_agent
   ```
2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**
   Copy environment variable template and configure:

   ```bash
   cp env.example .env
   ```

   Then edit the `.env` file and enter your actual API key:

   ```
   OPENAI_API_KEY=your OpenAI API key
   ```
4. **Run Application**

   ```bash
   streamlit run app.py
   ```

#### Method 3: Docker Deployment

1. **Build Image**

   ```bash
   docker build -t asd-agent .
   ```
2. **Run Container**

   ```bash
   docker run -p 8501:8501 -e OPENAI_API_KEY=your_key asd-agent
   ```

### Usage Instructions

1. **Start Application**: After running the above commands, the browser will automatically open the application interface
2. **Camera Authorization**: First-time use requires allowing camera access permissions
3. **Start Interaction**: Enter content in the text box, and the system will generate responses through the multi-agent framework
4. **Eye Tracking**: The system will automatically analyze the user's attention status

## Dependency Library Description

### Core Dependencies

- **numpy** (>=1.22.0): Numerical computation and array operations
- **opencv-python** (>=4.2.0.32): Computer vision and image processing
- **dlib** (>=19.16.0): Face detection and feature point recognition

### Web Framework

- **streamlit** (>=1.28.0): Web application development framework

### AI and Language Processing

- **langchain** (>=0.1.0): Large language model application framework
- **langchain-openai** (>=0.0.5): OpenAI model integration

### Utility Libraries

- **python-dotenv** (>=1.0.0): Environment variable management
- **websockets** (>=11.0.0): WebSocket communication

## Project Structure

```
ASD_agent/
├── app.py                      # Main application entry (Streamlit app)
├── multi_agent_framework.py    # Multi-agent framework
├── perception_agent.py         # Perception agent
├── decision_agent.py           # Decision agent
├── action_agent.py             # Action agent
├── example.py                  # Example code
├── test.py                     # Test code
├── requirements.txt            # Dependency library list
├── Dockerfile                  # Docker configuration file
├── gaze_tracking/              # Eye-tracking module
│   ├── __init__.py
│   ├── gaze_tracking.py        # Main tracking class
│   ├── eye.py                  # Eye detection
│   ├── pupil.py                # Pupil detection
│   ├── calibration.py          # Calibration functionality
│   └── trained_models/         # Pre-trained models
└── README.md                   # Project description
```

## Development Notes

### Code Standards

- All Python files contain detailed comments
- Use type hints to improve code readability
- Follow PEP 8 coding standards

### Extension Development

- Add new agents: Implement agent logic in corresponding files
- Modify interface: Edit Streamlit components in `app.py`
- Optimize eye tracking: Adjust parameters in the `gaze_tracking/` module

## Hugging Face Spaces Deployment

### Spaces Configuration Description

This project is configured to run directly on Hugging Face Spaces:

- **SDK**: Docker
- **Port**: 8501
- **Framework**: Streamlit
- **Tags**: streamlit, ai, healthcare, autism

### Environment Variable Configuration

In Hugging Face Spaces, you need to configure the following environment variables on the Settings page:

- `OPENAI_API_KEY`: Your OpenAI API key

### Important Notes

- Ensure the API key is valid and has sufficient quota
- Camera functionality may be limited in cloud environments
- It's recommended to test eye-tracking functionality in a local environment

### Security Reminders

⚠️ **Important Security Notice**:

- Never commit `.env` files containing real API keys to Git repositories
- Ensure `.env` files are added to `.gitignore`
- In Hugging Face Spaces, configure environment variables through the Settings page
- If API keys are accidentally leaked, regenerate them immediately

## Troubleshooting

### Common Issues

1. **Camera Cannot Access**

   - Check browser permission settings
   - Ensure camera is not occupied by other applications
2. **Dependency Installation Failed**

   - Ensure Python version compatibility
   - Try using a virtual environment
3. **API Call Failed**

   - Check if OpenAI API key is correct
   - Confirm network connection is normal

### Performance Optimization

- Adjust eye-tracking parameters to improve accuracy
- Optimize multi-agent response speed
- Adjust image processing parameters based on hardware configuration

## Contributing Guidelines

Welcome to submit Issues and Pull Requests to improve the project. Before submitting code, please ensure:

- Code passes all tests
- Add necessary documentation and comments
- Follow project coding standards

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contact Information

For questions or suggestions, please contact through:

- Submit GitHub Issue
- Send email to project maintainer

---

**Note**: This project is designed specifically for children with autism. Please ensure it is used under professional guidance and adjust interaction strategies according to specific needs.
