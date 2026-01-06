<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UMEQAM Dream Analyzer 🌙</title>
    <style>
        body {
            background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
            color: #e0e0ff;
            font-family: 'Segoe UI', Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 40px 20px;
        }
        h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #8a2be2;
        }
        p {
            font-size: 1.4em;
            margin-bottom: 30px;
        }
        textarea {
            width: 90%;
            max-width: 700px;
            height: 180px;
            background: rgba(255, 255, 255, 0.1);
            border: 3px solid #8a2be2;
            border-radius: 20px;
            color: white;
            padding: 20px;
            font-size: 1.3em;
            resize: vertical;
        }
        button {
            background: #8a2be2;
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 1.6em;
            border-radius: 50px;
            cursor: pointer;
            margin: 20px 10px;
            box-shadow: 0 0 30px #8a2be2;
            transition: 0.3s;
        }
        button:hover {
            background: #9932cc;
            transform: scale(1.05);
        }
        #result {
            margin-top: 50px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        #result h2 {
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        #result p {
            font-size: 1.4em;
            line-height: 1.8;
            margin: 20px 0;
        }
        #image {
            max-width: 100%;
            border-radius: 20px;
            margin: 30px 0;
            box-shadow: 0 0 40px #8a2be2;
        }
        .loading {
            font-size: 2em;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        .share-btn {
            background: #1da1f2;
        }
        #musicToggle {
            background: #4b0082;
        }
    </style>
</head>
<body>
    <h1>🌙 UMEQAM Dream Analyzer ✨</h1>
    <p>Опиши свой сон — получи этичный анализ и сюрреалистическую иллюстрацию от Grok AI</p>
    
    <textarea id="dreamText" placeholder="Я видел странный сон..."></textarea>
    <br>
    <button onclick="analyzeDream()">Анализировать сон</button>
    <button id="musicToggle">🔊 Медитация</button>
    
    <div id="result"></div>

    <audio id="backgroundMusic" loop>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        Ваш браузер не поддерживает аудио.
    </audio>

    <script>
        async function analyzeDream() {
            const dream = document.getElementById('dreamText').value.trim();
            if (!dream) {
                alert('Опиши свой сон!');
                return;
            }

            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p class="loading">Анализирую твой сон... 🌌</p>';

            try {
                const response = await fetch('https://umeqamdream.vercel.app/analyze-dream', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ dream_text: dream })
                });

                if (!response.ok) throw new Error('Ошибка сервера. Попробуй позже.');

                const data = await response.json();

                resultDiv.innerHTML = `
                    <h2>🌙 Анализ твоего сна от UMEQAM ✨</h2>
                    <p><strong>Эмоции 😌:</strong> ${data.emotions}</p>
                    <p><strong>Символы 🔮:</strong> ${data.symbols}</p>
                    <p><strong>Динамика ➡️:</strong> ${data.dynamics}</p>
                    <p><strong>Контекст 🌍:</strong> ${data.context}</p>
                    <p><strong>Мягкий вывод 💭:</strong> ${data.conclusion}</p>
                    <img id="image" src="${data.image_url}" alt="Иллюстрация твоего сна">
                    <p><em>#МойСон #UMEQAMdream</em></p>
                    <button class="share-btn" onclick="shareOnX()">Поделиться в X</button>
                `;
            } catch (error) {
                resultDiv.innerHTML = '<p style="color:red;">' + error.message + '</p>';
            }
        }

        function shareOnX() {
            const text = "Мой сон проанализировал UMEQAM AI 🌙 Это круто! Попробуй сам: https://umeqamdream.vercel.app #МойСон #UMEQAM";
            const url = "https://x.com/intent/post?text=" + encodeURIComponent(text);
            window.open(url, '_blank');
        }

        // Музыка
        const music = document.getElementById('backgroundMusic');
        const toggleButton = document.getElementById('musicToggle');
        let isPlaying = false;

        toggleButton.addEventListener('click', () => {
            if (isPlaying) {
                music.pause();
                toggleButton.textContent = '🔊 Медитация';
            } else {
                music.play();
                toggleButton.textContent = '🔇 Выключить';
            }
            isPlaying = !isPlaying;
        });
    </script>
</body>
</html>
