const app = require('./app');
const { connectDb } = require('./config/db');
const { env } = require('./config/env');

const start = async () => {
  await connectDb();

  app.listen(env.port, () => {
    console.log(`Payments service running on port ${env.port}`);
  });
};

start();

// Force nodemon restart to pick up updated .env changes

