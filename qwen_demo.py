
import sys
import os

print("=" * 60)
print("Qwen 千问模型本地演示 (7B 4-bit 量化版)")
print("=" * 60)

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
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
    
    model_name = "Qwen/Qwen2.5-7B-Instruct"
    print(f"\n📥 模型: {model_name}")
    print("   (使用 4-bit 量化，适合您的 GTX 1060 6GB)")
    
    try:
        print("\n⏳ 正在配置 4-bit 量化...")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        print("\n⏳ 正在加载模型和分词器 (首次运行会自动下载)...")
        print("   ⚠️  模型约 4-5GB，下载需要一些时间，请耐心等待...")
        print("   💡 使用国内镜像源加速下载...")
        
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        print("\n✅ 模型加载成功！")
        return model, tokenizer
        
    except Exception as e:
        print(f"\n❌ 模型加载失败: {e}")
        print("\n💡 提示:")
        print("   1. 如果显存不足，试试运行: python qwen_1.8b_demo.py")
        print("   2. 检查网络连接")
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
    
    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.95,
            do_sample=True
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
    print("欢迎使用 Qwen 千问 7B！")
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

