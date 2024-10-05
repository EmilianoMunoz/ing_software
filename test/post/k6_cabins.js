import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    iterations: 1400, // número total de iteraciones (solicitudes)
    insecureSkipTLSVerify: true, // Ignorar la verificación del certificado
};

export default function () {
    // Datos a enviar en el cuerpo de la solicitud POST
    let payload = JSON.stringify({
        type: 'Departamento',
        level: 'Estandar',
        capacity: '8'
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Realizar la solicitud POST
    let res = http.post('https://cabin.eden.localhost/api/v1/add', payload, params);

    // Verificar la respuesta
    check(res, {
        'status was 200': (r) => r.status === 200,
        'response body is not empty': (r) => r.body && r.body.length > 0,
    });
}
