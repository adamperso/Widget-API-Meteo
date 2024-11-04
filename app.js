import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

const app = express();
dotenv.config();

// Reste du code...

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

const API_KEY = process.env.OPENWEATHER_API_KEY;

app.get('/', (req, res) => {
    res.render('index', { weather: null, error: null });
});

// Mise en cache des données météo
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

app.post('/weather', async (req, res) => {
    const city = req.body.city;
    
    // Vérifier le cache
    if (cache.has(city)) {
        const cachedData = cache.get(city);
        if (Date.now() - cachedData.timestamp < CACHE_DURATION) {
            return res.render('index', { weather: cachedData.data, error: null });
        }
    }

    // Récupérer nouvelles données
    try {
        const data = await fetchWeatherData(city);
        cache.set(city, {
            data,
            timestamp: Date.now()
        });
        res.render('index', { weather: data, error: null });
    } catch (err) {
        res.render('index', { weather: null, error: 'Erreur' });
    }
});

async function fetchWeatherData(city) {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`;
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.cod === '404') {
        throw new Error('Ville non trouvée');
    }

    return {
        city: data.name,
        country: data.sys.country,
        temperature: Math.round(data.main.temp),
        description: data.weather[0].description,
        icon: data.weather[0].icon,
        humidity: data.main.humidity,
        windSpeed: data.wind.speed,
        feelsLike: Math.round(data.main.feels_like)
    };
}

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
