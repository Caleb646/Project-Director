import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import { useEffect, useState } from "react";

import { ApiClient } from "../services";
import { useAuthContext } from "../hooks";

interface returnedState<T> {
  data: T;
  loading: boolean;
  error: string | undefined;
}
export const useFetch = <T>(url: string, fetch?: boolean): returnedState<T> => {
  const signal = axios.CancelToken.source();
  const { getToken } = useAuthContext();
  const [state, setState] = useState<returnedState<T>>({
    data: ({ results: [] } as unknown) as T,
    loading: true,
    error: undefined,
  });
  const _get = async () => {
    const accessToken = await getToken(signal);

    const config: AxiosRequestConfig = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };
    ApiClient.get(url, config)
      .then((response: any) => {
        setState({
          data: response.data as T,
          loading: false,
          error: undefined,
        });
      })
      .catch((error: AxiosError) => {
        setState({
          data: ({ results: [] } as unknown) as T,
          loading: false,
          error: error.message,
        });
      });
  };
  useEffect(() => {
    if (fetch === true || fetch === undefined) {
      _get();
    }
    return () => {
      //clean up hanging or slow requests.
      console.log("cleaning up all of the requests");
      signal.cancel("Request was cancelled");
    };
  }, [url, fetch]);
  return state;
};
