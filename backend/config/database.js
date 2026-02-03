const { Pool } = require('pg');

const dbConfig = {
  development: {
    host: process.env.DATABASE_HOST || 'localhost',
    port: process.env.DATABASE_PORT || 5432,
    database: process.env.DATABASE_NAME || 'myapp_dev',
    user: process.env.DATABASE_USER || 'postgres',
    password: process.env.DATABASE_PASSWORD,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  },
  production: {
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false,
      ca: process.env.DATABASE_SSL_CERT
    },
    max: parseInt(process.env.DB_POOL_SIZE || '50'),
    idleTimeoutMillis: parseInt(process.env.DB_IDLE_TIMEOUT || '30000'),
  },
  test: {
    host: process.env.TEST_DATABASE_HOST || 'localhost',
    port: process.env.TEST_DATABASE_PORT || 5432,
    database: process.env.TEST_DATABASE_NAME || 'myapp_test',
    user: process.env.TEST_DATABASE_USER || 'postgres',
    password: process.env.TEST_DATABASE_PASSWORD
  }
};

const env = process.env.NODE_ENV || 'development';
const config = dbConfig[env];

const pool = new Pool(config);

pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

module.exports = { pool, config };
