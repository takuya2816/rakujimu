import axios from 'axios';
export default {
    outputLog(message) {
        console.log(`LOG: ${message}`)
    },

    async gateway_get(apiurl, data){
        if (data) {
            try {
                const response = await axios.get(apiurl,{params:{data}});  // クエリパラメタ
                console.log(response);
                return response.data;
            } catch (error) {
                alert("Error: " + error);
            }
        }else{
            try {
                const response = await axios.get(apiurl);
                return response.data;
            } catch (error) {
                alert("Error: " + error);
            }
        }
    },
    async gateway_post(apiurl, data){
        try {
            const response = await axios.post(apiurl, data);  // リクエストボディ
            console.log(response);
            return response.data;
        } catch (error) {
            alert("Error: " + error);
        }
    },
}