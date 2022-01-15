import axios, { AxiosError, AxiosResponse, AxiosRequestConfig } from "axios";
class ApiRequestClient {
  constructor() {
    //axios.defaults.withCredentials = true;
    // if (window.location.origin === "http://localhost:3000")
    // {
    //axios.defaults.baseURL = "http://localhost:8000";
    // }
    // else
    // {
    //     axios.defaults.baseURL = window.location.origin;
    // }

    //axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    //axios.defaults.xsrfCookieName = "csrftoken";
    //axios.defaults.withCredentials = true;
    //axios.defaults.baseURL = "http://localhost:8000";

    //pass to a get request to download a file
    const fileDowloadConfig: AxiosRequestConfig = {
      responseType: "blob",
      timeout: 30000,
    };
  }

  public get(
    url: string,
    config?: AxiosRequestConfig | undefined
  ): Promise<AxiosResponse<any> | AxiosError> {
    return new Promise((resolve, reject) => {
      axios
        .get(url, config)

        .then((response: AxiosResponse<any>) => {
          console.log("get request data: ", response);
          resolve(response);
        })
        .catch((error: AxiosError) => {
          console.log("get request failed because: ", error.message);
          reject(error);
        });
    });
  }

  public post(
    url: string,
    data: any,
    config?: AxiosRequestConfig | undefined
  ): Promise<AxiosResponse<any> | AxiosError> {
    return new Promise((resolve, reject) => {
      axios
        .post(url, data, config)
        .then((response: AxiosResponse<any>) => {
          console.log("successful post request: ", response);
          resolve(response);
        })
        .catch((error: AxiosError) => {
          console.log("post request failed because: ", error.response);
          reject(error);
        });
    });
  }

  public patch(
    url: string,
    data: any,
    config?: AxiosRequestConfig | undefined
  ): Promise<AxiosResponse<any> | AxiosError> {
    return new Promise((resolve, reject) => {
      axios
        .patch(url, data, config)

        .then((response: AxiosResponse<any>) => {
          response.request;
          resolve(response);
        })
        .catch((error: AxiosError) => {
          reject(error);
        });
    });
  }
}

export const ApiClient = new ApiRequestClient();
