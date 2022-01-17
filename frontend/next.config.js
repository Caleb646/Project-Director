module.exports = {
  future: {
    webpack5: true,
  },
  distDir: "build", //set "next build" output directory

  webpackDevMiddleware: (config) => {
    /*
     * Allows for hot reloading while running inside a Docker container.
     * Polls for changes once a second.
     */
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },

  //excludeFile: (str) => /\*.{spec,test}.js/.test(str),
  // async rewrites() {
  //   return [
  //     {
  //       source: "/api/auth/user/register/",
  //       destination: `http://localhost:8000/pm/api/auth/user/register/`,
  //     },
  //     {
  //       source: "/api/auth/user/login/",
  //       destination: `http://localhost:8000/pm/api/auth/user/login/`,
  //     },
  //   ];
  // },
};
