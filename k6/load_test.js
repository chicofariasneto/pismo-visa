import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 20  }, // ramp up to baseline
    { duration: '1m',  target: 20  }, // hold baseline
    { duration: '30s', target: 50  }, // ramp up to stress
    { duration: '1m',  target: 50  }, // hold stress
    { duration: '30s', target: 100 }, // spike
    { duration: '30s', target: 0   }, // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    errors: ['rate<0.01'],
  },
};

export function setup() {
  const res = http.post(
    `${BASE_URL}/api/v1/accounts/`,
    JSON.stringify({ document_number: '12345678900' }),
    { headers: { 'Content-Type': 'application/json' } },
  );

  if (res.status !== 201) {
    throw new Error(`Setup failed: could not create account (status ${res.status})`);
  }

  return { accountId: res.json('account_id') };
}

export default function (data) {
  const res = http.post(
    `${BASE_URL}/api/v1/transactions/`,
    JSON.stringify({
      account_id: data.accountId,
      operation_type_id: 1,
      amount: -100.00,
    }),
    { headers: { 'Content-Type': 'application/json' } },
  );

  const ok = check(res, {
    'status 201': (r) => r.status === 201,
    'response < 500ms': (r) => r.timings.duration < 500,
  });

  errorRate.add(!ok);
  sleep(0.5);
}
