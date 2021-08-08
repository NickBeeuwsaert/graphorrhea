export class APIError extends Error {}
export class APIClientError extends APIError {}
export class APIServerError extends APIError {}
export class AuthenticationError extends APIClientError {}

/**
 * Helper for checking if a status code is in a particular range
 *
 * @param {number} start
 * @param {number} end
 * @returns {function(number): boolean}
 */
const inRange = (start, end) => (v) => start <= v && v < end;

const isSuccess = inRange(200, 299);
const isClientError = inRange(400, 499);
const isServerError = inRange(500, 599);

export default class Graphorrhea {
  /**
   *
   * @param {URL} baseURL
   * @param {typeof fetch} fetch
   */
  constructor(baseURL, fetch = self.fetch) {
    this.baseURL = new URL(baseURL);
    this.fetch = fetch;
  }

  _endpoint(method, params) {
    params = new URLSearchParams(params);
    const endpoint = new URL(method, this.baseURL);

    for (const [name, value] of params.entries()) {
      endpoint.searchParams.append(name, value);
    }

    return endpoint;
  }

  /**
   *
   * @param {"GET"|"POST"|"DELETE"|"PUT"|"PATCH"} method
   * @param {string} apiMethod
   * @param {RequestInit} init
   */
  _makeRequest(method, apiMethod, init = {}) {
    const headers = new Headers(init.headers);

    // Always send and receive JSON
    headers.set("Content-Type", "application/json");
    headers.set("Accept", "application/json");

    return this.fetch(this._endpoint(apiMethod), {
      method,
      ...init,
      headers,
    }).then((response) => {
      if (isServerError(response.status)) throw new APIServerError();
      if (isClientError(response.status)) {
        if (response.status == 403) throw new AuthenticationError();
        throw new APIClientError();
      }
      return response;
    });
  }

  async login(username, password) {
    const response = await this._makeRequest("POST", "auth/login", {
        body: JSON.stringify({ username, password }),
      }),
      body = await response.json();

    return {
      accessToken: body["token"],
      refreshToken: body["refresh_token"],
    };
  }
  async register(username, password) {
    const response = await this._makeRequest("POST", "auth/register", {
      body: JSON.stringify({ username, password }),
    });

    return await response.json();
  }

  async getResource(path) {
    const response = await this._makeRequest(
        "GET",
        this._endpoint("files", { path })
      ),
      body = await response.json();

    return body;
  }

  async writeNote(path, content) {
    const response = await this._makeRequest(
        "POST",
        this._endpoint("files", { path: "/" }),
        { body: JSON.stringify({ type: "note", name: path, content: content }) }
      ),
      body = await response.json();

    return body;
  }
}
