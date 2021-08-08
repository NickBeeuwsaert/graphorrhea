/**
 *
 * @param {(function(Request): Request)[]} requestTransformers
 * @param {(function(Promise): Promise)[]} responseTransformers
 * @param {function(Request): Promise} fetchImplementation
 * @returns {function(Request): Promise<Response>}
 */

export default (
    requestTransformers = [],
    responseTransformers = [],
    fetchImplementation = self.fetch
  ) =>
  (request) => {
    const transformedRequest = requestTransformers.reduce(
      (request, transformer) => transformer(request),
      request
    );

    return responseTransformers.reduce(
      (promise, transformer) => transformer(promise),
      fetchImplementation(transformedRequest)
    );
  };
