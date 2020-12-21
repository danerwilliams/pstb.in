module.exports = {

  siteMetadata: {
    title: "pstbin",
  },

  plugins: [
    {
        resolve: `gatsby-plugin-s3`,
        options: {
            bucketName: 'dane-test-bucket',
        },
    },
  ]
};
