import os
import sys
import requests
from tqdm import tqdm
import huggingface_hub

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def download_model():
    """
    Download the Llama 3 model from Hugging Face.
    """
    model_name = "TheBloke/Llama-3-8B-Instruct-GGUF"
    filename = "llama-3-8b-instruct.Q4_K_M.gguf"
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, filename)
    
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return model_path
    
    print(f"Downloading {filename} from {model_name}...")
    
    try:
        # Download using huggingface_hub
        huggingface_hub.hf_hub_download(
            repo_id=model_name,
            filename=filename,
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"Model downloaded successfully to {model_path}")
        return model_path
        
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        print("\nManual download instructions:")
        print(f"1. Go to https://huggingface.co/{model_name}/tree/main")
        print(f"2. Download the file {filename}")
        print(f"3. Place it in the models directory at {models_dir}")
        return None

if __name__ == "__main__":
    download_model()
