import http from 'k6/http';
import { sleep, check } from 'k6';



export let options = {
    vus: 200, // número de usuarios virtuales
    duration: '8s', // duración total de la prueba
  };
  

export default function () {
    let res = http.get('https://user.eden.localhost/api/v1/all');
    check(res, {
      'status was 200': (r) => r.status === 200,
      'response body contains users': (r) => r.body.includes('users'),
    });
    sleep(1);
  }
