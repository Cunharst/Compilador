import os
import time
import requests
from openai import OpenAI
from lumaai import LumaAI
# Ajustado o import do MoviePy para evitar erros de resolução de submódulos nas versões estáveis
from moviepy.editor import VideoFileClip, concatenate_videoclips

# --- CONFIGURAÇÃO DAS CHAVES DE API ---
# Substitua os valores abaixo pelas suas chaves reais ou configure as variáveis de ambiente
OPENAI_API = os.environ.get("OPENAI_API_KEY", "SUA_CHAVE_OPENAI_AQUI")
LUMA_API = os.environ.get("LUMA_API_KEY", "SUA_CHAVE_LUMA_AQUI")

# Inicialização dos clientes das APIs
client_gpt = OpenAI(api_key=OPENAI_API)
client_luma = LumaAI(auth_token=LUMA_API)

def criar_cenas_cinematograficas():
    print("🤖 GPT criando o conceito visual do vídeo...")
    prompt = (
        "Create a list of 3 short, separate visual scene descriptions for a mysterious TikTok video about Atlantis. "
        "Each scene must be a single line, described in English, focusing strictly on cinematic visuals, 4k, hyper-realistic, 9:16 aspect ratio. "
        "Do not include numbering, markdown bolding (**), or introductory text. Just the raw prompts separated by newlines."
    )
    
    response = client_gpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Divide a resposta por quebra de linha e limpa espaços vazios
    conteudo = response.choices[0].message.content
    cenas = [linha.strip() for linha in conteudo.split('\n') if linha.strip()]
    
    # Retorna no máximo as 3 primeiras cenas limpas
    return cenas[:3]

def gerar_video_por_ia(prompt_visual, index):
    print(f"\n🎬 [Cena {index}] Solicitando geração de vídeo para a IA...")
    
    # Dispara o job de geração do vídeo na API da Luma
    generation = client_luma.generations.create(
        prompt=prompt_visual,
        aspect_ratio="9:16"  # Mantém o padrão vertical do TikTok
    )
    
    # Loop de checagem (Polling) para aguardar a renderização na nuvem
    while True:
        status_check = client_luma.generations.get(id=generation.id)
        
        if status_check.state == "completed":
            # Acessa a URL do vídeo gerado de forma segura dentro do objeto de assets
            video_url = status_check.assets.video
            print(f"✅ [Cena {index}] Renderização concluída na nuvem!")
            break
        elif status_check.state == "failed":
            raise Exception(f"A IA falhou ao processar a renderização da Cena {index}.")
            
        print(f"⏳ [Cena {index}] Ainda processando na nuvem... aguardando 15 segundos...")
        time.sleep(15)
        
    # Realiza o download do arquivo .mp4 gerado pela API
    filename = f"cena_{index}.mp4"
    print(f"📥 Baixando arquivo da Cena {index}...")
    resposta_video = requests.get(video_url, stream=True)
    
    if resposta_video.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in resposta_video.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    else:
        raise Exception(f"Não foi possível baixar o vídeo gerado da URL fornecida.")

def montar_filme_final(lista_videos, output_path="resultado_cinematografico.mp4"):
    print("\n🎥 Iniciando a montagem e concatenação dos clipes gerados...")
    
    # Cria uma lista de objetos VideoFileClip
    clipes = []
    for path in lista_videos:
        if os.path.exists(path):
            clipes.append(VideoFileClip(path))
    
    if not clipes:
        print("⚠️ Nenhum arquivo de vídeo válido foi encontrado para montagem.")
        return

    # Junta os pedaços de vídeo em sequência linear
    video_final = concatenate_videoclips(clipes, method="compose")
    
    # Exporta o arquivo final otimizado para web/redes sociais
    print(f"💾 Renderizando arquivo final localmente: {output_path}")
    video_final.write_videofile(
        output_path, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac",
        threads=4
    )
    
    # Fecha os descritores de arquivo para liberar o disco do Windows de travas
    for c in clipes: 
        c.close()
    video_final.close()
    print(f"✨ Vídeo Cinematográfico salvo com sucesso: {output_path}")

# --- Fluxo Executável Principal ---
if __name__ == "__main__":
    # Garante que as chaves padrão foram substituídas antes de rodar
    if "SUA_CHAVE" in OPENAI_API or "SUA_CHAVE" in LUMA_API:
        print("❌ Erro: Substitua 'SUA_CHAVE' pelas suas credenciais reais da OpenAI e LumaAI no código.")
    else:
        # 1. Planeja os prompts visuais de IA
        prompts_das_cenas = criar_cenas_cinematograficas()
        print(f"📋 Cenas planejadas pela IA:\n" + "\n".join([f"- {p}" for p in prompts_das_cenas]))
        
        arquivos_de_video = []
        
        # 2. Loop de processamento de cada cena de vídeo
        for idx, prompt in enumerate(prompts_das_cenas, start=1):
            try:
                video_local = gerar_video_por_ia(prompt, idx)
                arquivos_de_video.append(video_local)
            except Exception as e:
                print(f"❌ Erro crítico na execução da cena {idx}: {e}")
                
        # 3. Se houver vídeos gerados, agrupa no arquivo final
        if arquivos_de_video:
            montar_filme_final(arquivos_de_video)