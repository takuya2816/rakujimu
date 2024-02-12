import axios from 'axios';
export default {
    outputLog(message) {
        console.log(`LOG: ${message}`)
    },

    async gateway_get(apiurl){
        try {
            const response = await axios.get(apiurl);
            return response.data;
        } catch (error) {
            alert("Error: " + error);
        }
    },
    async gateway_post(apiurl, data){
        var jsonData = JSON.stringify(data);
        var headers =  {
            headers: {'Content-Type': 'application/json'}
        };
        try {
            const response = await axios.post(apiurl, jsonData, headers);
            console.log(response);
            return response.data;
        } catch (error) {
            alert("Error: " + error);
        }
    },
}