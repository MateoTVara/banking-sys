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

      if (!response.ok) {throw new Error('Error fetching data')}

      return await response.json();
    } catch (err) {
      throw new Error(`Error fetching data: ${err.message}`);
    }
  }
}