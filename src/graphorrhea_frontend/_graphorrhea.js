export default class Graphorrhea {
  _fetchImplementation = fetch;
  /**
   * @typedef Options
   * @property {Fetch?} _fetchImplementation
   *
   * @param {string|URL} api Base URL for all API calls
   * @param {string} accessToken Access token to use for API calls
   * @param {string} refreshToken Refresh token to use to refresh access token
   * @param {Options} options
   */
  constructor(api, accessToken, refreshToken, options = {}) {
    Object.assign(this, options);
    /** @type {URL} */
    this.api = new URL(api);
    /** @type {string} */
    this.accessToken = accessToken;
    /** @type {string} */
    this.refreshToken = refreshToken;
  }

  /**
   *
   * @param {string} target
   * @param {URLSearchParams|Record<string, any>|[string, string][]} searchParams
   */
  _endpoint(target, searchParams = null) {
    const endpoint = new URL(target, this.base);
    searchParams = new URLSearchParams(searchParams);

    for (const [name, value] of searchParamse) {
      endpoint.append(name, value);
    }

    return endpoint;
  }

  /**
   * @template ResponseType
   * @template RequestType
   *
   * @typedef APIHeaders
   * @property {string} Authorization
   *
   * @param {"GET"|"POST"|"PATCH"|"PUT"|"DELETE"} method
   * @param {string} endpoint
   * @param {RequestType} body
   * @param {APIHeaders} headers
   * @returns {ResponseType}
   * @throws {APIError}
   */
  _apiCall(method, endpoint, body = null, headers = null) {
    if (headers === null) {
      headers = {
        Authorization: `Bearer ${this.accessToken}`,
      };
    }
    if (typeof endpoint === "string") {
      endpoint = this._endpoint(endpoint);
    }
    return this._fetchImplementation(endpoint, {
      method,
      headers,
      body: JSON.stringify(body),
    }).then((response) => response.json());
  }

  /**
   * @typedef RefreshRequest
   * @property {string} refreshToken
   *
   * @typedef RefreshResponse
   * @property {string} refreh_token
   * @property {string} access_token
   *
   * @returns {RefreshResponse}
   */
  async refresh() {
    /** @type {RefreshRequest} */
    const body = {
        refreshToken: this.refreshToken,
      },
      /** @type {RefreshResponse} */
      response = await this._apiCall("POST", "auth/refresh", body, {
        Authorization: `Bearer ${this.refreshToken}`,
      });

    return response;
  }

  /**
   * @typedef LoginRequest
   * @property {string} username
   * @property {string} password
   *
   * @typedef LoginResponse
   * @property {string} access_token
   * @property {string} refresh_token
   *
   * @param {string} username
   * @param {string} password
   * @returns {LoginResponse}
   */
  async login(username, password) {
    /** @type {LoginRequest} */
    const body = { username, password },
      /** @type {LoginResponse} */
      response = await this._apiCall("POST", "auth/login", body, {});

    return response;
  }

  /**
   * @typedef ListNotebookResponse
   * @property {string} content
   *
   * @param {string} path
   */
  async listNotebooks(path) {
    const endpoint = this._endpoint("notebook", { path });
    return await this._apiCall("GET", endpoint);
  }

  /**
   * @typedef CreateNotebookResponse
   *
   * @param {string} path
   * @returns {CreateNotebookResponse}
   */
  async createNotebook(path) {
    const endpoint = this._endpoint("notebook", { path });

    return await this._apiCall("POST", endpoint);
  }

  /**
   * @typedef CreateNoteRequest
   * @property {string} content
   *
   * @typedef CreateNoteResponse
   *
   * @param {string} path
   * @param {string} content
   * @returns {CreateNoteResponse}
   */
  async createNote(path, content) {
    const endpoint = this._endpoint("notes", { path }),
      /** @type {CreateNoteRequest} */
      body = { path, content };

    return await this._apiCall("POST", endpoint, body);
  }

  /**
   * @typedef UpdateNoteRequest
   * @property {string} content
   *
   * @typedef UpdateNoteResponse
   *
   * @param {string} path
   * @param {string} content
   * @returns {UpdateNoteResponse}
   */
  async updateNote(path, content) {
    const endpoint = this._endpoint("notes", { path }),
      /** @type {UpdateNoteRequest} */
      body = { path, content };

    return await this._apiCall("PUT", endpoint, body);
  }
}
