
import sys
import os

print("=" * 60)
print("Qwen 千问模型本地演示 (1.8B 轻量版)")
print("=" * 60)

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    print("\n✅ 依赖库导入成功")
except ImportError as e:
    print(f"\n❌ 缺少依赖库: {e}")
    print("请先运行: python install_qwen.py")
    sys.exit(1)

def setup_model():
    print("\n" + "=" * 60)
    print("正在设置模型...")
    print("=" * 60)
    
    model_name = "Qwen/Qwen1.5-1.8B-Chat"
    print(f"\n📥 模型: {model_name}")
    print("   (轻量级模型，运行流畅)")
    
    try:
        print("\n⏳ 正在加载模型和分词器 (首次运行会自动下载)...")
        print("   💡 使用国内镜像源加速下载...")
        
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True
        )
        
        print("\n✅ 模型加载成功！")
        return model, tokenizer
        
    except Exception as e:
        print(f"\n❌ 模型加载失败: {e}")
        print("\n💡 提示:")
        print("   1. 确保网络连接正常")
        return None, None

def chat(model, tokenizer, prompt, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95
    )
    
    generated_ids = [
        output_ids[len(input_ids):] 
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def main():
    model, tokenizer = setup_model()
    if model is None:
        return
    
    print("\n" + "=" * 60)
    print("欢迎使用 Qwen 千问 1.8B！")
    print("=" * 60)
    print("\n输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清屏\n")
    
    while True:
        try:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
                
            if user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
                
            if not user_input:
                continue
                
            print("\n🤖 Qwen: ", end="", flush=True)
            
            response = chat(model, tokenizer, user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 出错了: {e}")

if __name__ == "__main__":
    main()

