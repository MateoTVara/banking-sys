export class ApiManager {
  constructor() {

  }

  static async fetchData(url, formData){
    try {
      if (typeof url !== 'string'){throw new TypeError('url must be a string')}

      const response = await fetch(url, {
        method: 'POST', 
        body: formData,
      });

      const data = await response.json();
      
      return data;
    } catch (err) {
      return { error: `Error de conexión: ${err.message}` };
    }
  }
}