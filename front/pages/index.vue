<!-- LINEIDから顧客・提供者振り分けて各トップ画面へリダイレクト -->

<template>
    <div>   
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            accessToken: "",
        }
    },
    mounted() {
        this.$liffInit
        .then(() => {
            pass
        })
        .catch((error) => {
            this.liffError = error;
        });
    },

    methods: {
        async getAccessToken(){  // ユーザのaccesstokenを取得
            try {
                const accessToken = liff.getAccessToken();
                return accessToken
            } catch (error) {
                console.error(error);
                return null
            }
        },
        async getUserProfile(accessToken) {  // ユーザ情報を取得
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
        },
        async getUserInfo() {
            const accessToken = await this.getAccessToken();
            if (accessToken) {
                await this.getUserProfile(accessToken);
            }
        },
    },
};
</script>