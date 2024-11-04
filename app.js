import fetch from 'node-fetch';
import express from 'express';
import dotenv from 'dotenv';

dotenv.config();const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

const API_KEY = process.env.OPENWEATHER_API_KEY;

app.get('/', (req, res) => {
    res.render('index', { weather: null, error: null });
});

app.post('/weather', async (req, res) => {
    const city = req.body.city;
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.cod === '404') {
            res.render('index', {
                weather: null,
                error: 'Ville non trouvée'
            });
            return;
        }

        const weather = {
            city: data.name,
            country: data.sys.country,
            temperature: Math.round(data.main.temp),
            description: data.weather[0].description,
            icon: data.weather[0].icon,
            humidity: data.main.humidity,
            windSpeed: data.wind.speed,
            feelsLike: Math.round(data.main.feels_like)
        };

        res.render('index', { weather, error: null });
    } catch (err) {
        res.render('index', {
            weather: null,
            error: 'Erreur lors de la récupération des données'
        });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
