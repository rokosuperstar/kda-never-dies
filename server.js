const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
// Dôležité: Použi process.env.PORT, ktorý nastavuje Railway/Render/Cyclic
const PORT = process.env.PORT || 3000;

// Povoliť všetky CORS requesty
app.use(cors());

// Slúžiť celý spacemap priečinok ako public
app.use('/', express.static(path.join(__dirname, 'spacemap')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});
// Logger voliteľný
app.use((req, res, next) => {
  console.log(`[REQ] ${req.method} ${req.url}`);
  next();
});

// 404 fallback
app.use((req, res) => {
  res.status(404).send('404 Not Found');
});

// Nepíš tam localhost!
app.listen(PORT, () => {
  console.log(`🌍 Server beží na porte ${PORT}`);
});
