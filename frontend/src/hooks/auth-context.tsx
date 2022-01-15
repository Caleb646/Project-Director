//@ts-nocheck

import React, { useState, useEffect, useContext } from "react";

import {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse,
  CancelTokenSource,
} from "axios";

import { ApiClient } from "../services";
import { apiPaths } from "../components";
import { settings } from "..";

interface User {
  email: string;
}

const fetchAccessToken = (
  data: FormData
): Promise<AxiosResponse<any> | AxiosError> => {
  return ApiClient.post(apiPaths.login, data, { withCredentials: true });
};

const refreshAccessToken = (
  cancelSignal?: CancelTokenSource
): Promise<AxiosResponse<any> | AxiosError> => {
  const cancelToken =
    cancelSignal === undefined ? undefined : cancelSignal.token;
  const config: AxiosRequestConfig = {
    withCredentials: true,
    cancelToken: cancelToken,
  };
  return ApiClient.post(apiPaths.tokenRefresh, {}, config);
};

async function fetchUser(
  token: string,
  cancelSignal?: CancelTokenSource
): Promise<AxiosResponse<any> | AxiosError> {
  const cancelToken =
    cancelSignal === undefined ? undefined : cancelSignal.token;
  const config: AxiosRequestConfig = {
    cancelToken: cancelToken,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  return ApiClient.get(apiPaths.whoAmI, config);
}

type AuthContextProps = {
  isAuthenticated: boolean;
  loading: boolean;
  user: User | null;
  login: (username: string, password: string) => Promise<Response>;
  logout: () => void;
  getToken: () => Promise<string>;
};

const AuthContext = React.createContext<Partial<AuthContextProps>>({});

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider = ({
  children,
}: AuthProviderProps): React.ReactNode => {
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string>("");
  const [accessTokenExpiry, setAccessTokenExpiry] = useState<number | null>(
    null
  );

  const setNotAuthenticated = (): void => {
    setIsAuthenticated(false);
    setLoading(false);
    setUser(null);
  };

  const accessTokenIsValid = (): boolean => {
    if (accessToken === "") {
      //console.log("access token is not valid");
      return false;
    }
    if (accessTokenExpiry === null) return false;
    const expiry = new Date(accessTokenExpiry);
    //console.log("Checking token expiry:", expiry);
    return expiry.getTime() > Date.now();
  };

  const initAuth = async (cancelSignal: CancelTokenSource): Promise<void> => {
    setLoading(true);
    if (!accessTokenIsValid()) {
      console.log("Invalid access token so refetching");
      //access token could not be refresh so set user as not authenticated
      refreshToken(cancelSignal).catch((error: AxiosError) => {
        setNotAuthenticated();
      });
    } else {
      setIsAuthenticated(true);
      setLoading(false);
    }
  };

  // useEffect(() => {
  //   console.log("authing user!!!!!!");
  //   initAuth();
  // }, []);

  const initUser = async (
    token: string,
    cancelSignal?: CancelTokenSource
  ): Promise<AxiosResponse | AxiosError> => {
    return new Promise((resolve, reject) => {
      fetchUser(token, cancelSignal)
        .then((response: any) => {
          setUser(response.data.results);
          resolve(response.data);
        })
        .catch((error: any) => {
          //console.trace("initUser Failed: ", error);
          reject(error);
        });
    });
  };

  const refreshToken = async (
    cancelToken: CancelTokenSource
  ): Promise<string | AxiosError> => {
    /*
    If there is a valid refresh token stored as a httponly cookie the access token will be
    refreshed, and then put back into state. User info if null will also be refetched using the new access token.

    If the refresh attempt fails the user is set as not authenticated.
    */
    setLoading(true);
    return new Promise((resolve, reject) => {
      refreshAccessToken(cancelToken)
        .then((response: any) => {
          const { accessToken, accessExpire } =
            getTokenAndExpireFromResponse(response);
          handleNewToken(accessToken, accessExpire);
          if (user === null) {
            //console.log("No user loaded so loading from access token");
            initUser(accessToken, cancelToken);
          }
          return resolve(accessToken);
        })
        .catch((error: any) => {
          console.log("user token could not be refreshed: ", error);
          setNotAuthenticated();
          return reject(error);
        });
    });
  };

  const handleNewToken = (accessToken: string, accessExpire: any): void => {
    //console.log("token: ", accessToken, "expiration: ", accessExpire);
    setAccessToken(accessToken);
    const expiryInt = accessExpire * 1000;
    setAccessTokenExpiry(expiryInt);
    setIsAuthenticated(true);
    setLoading(false);
  };

  const register = async (
    data: FormData,
    cancelSignal?: CancelTokenSource
  ): Promise<AxiosResponse<any> | AxiosError> => {
    setLoading(true);
    //has to have withCredentials: true to receive the refresh token.
    return ApiClient.post(apiPaths.confirmRegistration, data, {
      withCredentials: true,
    })
      .then((response: AxiosResponse<any>) => {
        const { accessToken, accessExpire } =
          getTokenAndExpireFromResponse(response);
        handleNewToken(accessToken, accessExpire);
        initUser(accessToken, cancelSignal);
        //without this the IsAuthenticated will never be set to true.
        //initAuth(cancelSignal);
        setIsAuthenticated(true);
        setLoading(false);
        return Promise.resolve(response);
      })
      .catch((error: AxiosError) => Promise.reject(error));
  };

  const login = async (
    data: FormData,
    cancelSignal?: CancelTokenSource
  ): Promise<any> => {
    console.log("login data: ", data);
    setLoading(true);
    return new Promise((resolve, reject) => {
      fetchAccessToken(data)
        .then((response: any) => {
          const { accessToken, accessExpire } =
            getTokenAndExpireFromResponse(response);
          handleNewToken(accessToken, accessExpire);
          initUser(accessToken, cancelSignal);
          setLoading(false);
          return resolve(response);
        })
        .catch((error: any) => {
          setIsAuthenticated(false);
          setLoading(false);
          return reject(error);
        });
    });
  };

  const logout = (): void => {
    setAccessToken("");
    setAccessTokenExpiry(null);
    setNotAuthenticated();
    ApiClient.post(apiPaths.logout, {}, { withCredentials: true });
  };

  const getTokenAndExpireFromResponse = (
    response: AxiosResponse
  ): { accessToken: string; accessExpire: any } => {
    // console.log(
    //   "token: ",
    //   response.data[settings.ACCESS_TOKEN],
    //   "expiration: ",
    //   response.data[settings.ACCESS_TOKEN_EXPIRE]
    //);
    return {
      accessToken: response.data[settings.ACCESS_TOKEN],
      accessExpire: response.data[settings.ACCESS_TOKEN_EXPIRE],
    };
  };

  const getToken = async (
    cancelSignal: CancelTokenSource
  ): Promise<string | AxiosError> => {
    // Returns an access token if there's one or refetches a new one
    //console.log("Getting access token..");

    return new Promise((resolve, reject) => {
      if (accessTokenIsValid()) {
        console.log("Getting access token.. existing token still valid");
        return resolve(accessToken);
      } else if (loading) {
        return resolve(accessToken);
      } else {
        console.log("Getting access token.. getting a new token");
        return refreshToken(cancelSignal)
          .then((token) => resolve(token))
          .catch((error) => reject(error));
      }
    });
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    register,
    getToken,
    initAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuthContext = (): any => useContext(AuthContext);
