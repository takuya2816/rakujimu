import liff from '@line/liff'

export default (context, inject) => {
  // 開発のためliffコメントアウト
  inject('liff', liff)
  // const initResult = liff
  //   .init({ liffId: '2004834715-qM4Eadxd' })
  //   .then(() => {
  //     if (!liff.isLoggedIn()) {
  //       liff.login()
  //     }
  //     console.log('liff.init() done')
  //   })
  //   .catch((error) => {
  //     console.log(`liff.init() failed: ${error}`)
  //     if (!process.env.liffId) {
  //       console.info(
  //         'LIFF Starter: Please make sure that you provided `LIFF_ID` as an environmental variable.'
  //       )
  //     }
  //     return Promise.reject(error)
  //   })
  // You can access liff.init()'s return value (Promise object)
  // as this.$liffInit() by inject()
  // inject('liffInit', initResult)
}
