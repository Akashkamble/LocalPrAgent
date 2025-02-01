# Local Pull Request Agent

A streamlined pull request review tool which uses local LLM to review the code.

This is just POC project to learn how to use Ollama effectively and this project is inspired by [qodo-ai](https://github.com/qodo-ai/pr-agent/tree/main).

## Working
![Image](https://github.com/user-attachments/assets/26ed9ce4-edd3-42c2-89d6-962fbaf161bb)

## Setup

1. Install [Ollama]("https://ollama.com/") in your machine if not already installed:
2. Download the model 
```bash
  ollama pull <model_name>
```

3. After you have downloaded the model, you can start the Ollama service by running the following command:
```bash
  ollama serve
```

3. Edit `settings/configuration.toml` with your settings:
```toml
[config]
git_provider = "github"
publish_output = true    # whether to post comments to PR
review_score_threshold = 95 # This should be between [0-100]. The minimum score required to comment on the PR
pr_link = "" # The PR link on which you want to comment

[ollama]
api_base = "http://localhost:11434"
model = "model-name-which-you-downloaded using ollama pull"
temperature = 0.1 # This should be between [0-1]. The higher the value, the more creative the output

[github]
token = "your-github-personal-access-token"    # Get from https://github.com/settings/tokens
```

## Features

- Currently only Supports GitHub. 
- Uses locally installed Ollama.
- Comments on PRs if LLM Review score is less than the threshold set by you.


### After completing setup you can try this by running main.py
