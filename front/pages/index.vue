<template>
    <div>
        <p v-if="lineId">LINE ID: {{ lineId }}</p>
        <p v-if="displayName">LINE Name: {{ displayName }}</p>
        <p v-if="pictureUrl">LINE icon: {{ pictureUrl }}</p>
        <button @click="getUserInfo">Get LINE ID</button>
    </div>
</template>
    
<script>
import axios from 'axios'

export default {
    data: function() {
        return {
            lineId: "",
            displayName: "",
            pictureUrl: "",
            getUserInfo: "",
        };
    },
    mounted() {
        this.$liffInit
        .then(() => {
            const getAccessToken = async () => {  // ユーザのaccesstokenを取得
                try {
                    const accessToken = liff.getAccessToken();
                    return accessToken
                } catch (error) {
                    console.error(error);
                    return null
                }
            }

            const getUserProfile = async (accessToken) => {  // ユーザ情報を取得
                try {
                    const response = await axios.get(`https://api.line.me/v2/profile`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                    });
                    this.lineId = response.data.userId;  // 各種を更新
                    this.displayName = response.data.displayName;
                    this.pictureUrl = response.data.pictureUrl;
                } catch (error) {
                    console.error(error);
                }
            }

            this.getUserInfo = async () => {
                const accessToken = await getAccessToken();
                if (accessToken) {
                    await getUserProfile(accessToken);
                }
            }
        })
        .catch((error) => {
        this.liffError = error;
        });
        console.log(this);
    }
}
</script>