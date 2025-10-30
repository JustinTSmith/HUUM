import Foundation
import SwiftUI

@MainActor
final class SaunaViewModel: ObservableObject {
    @Published var isHeating: Bool = false
    @Published var currentTemperature: Int?
    @Published var targetTemperature: Int = 70
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        decoder = JSONDecoder()
        Task { await refreshStatus() }
    }

    func refreshStatus() async {
        await performRequest(endpoint: "api/sauna/status") { data in
            let status = try self.decoder.decode(SaunaStatus.self, from: data)
            self.isHeating = status.statusCode == 231
            self.currentTemperature = Int(status.temperature)
            self.targetTemperature = Int(status.targetTemperature) ?? self.targetTemperature
        }
    }

    func toggleSauna() async {
        if isHeating {
            await stopSauna()
        } else {
            await startSauna()
        }
    }

    func startSauna() async {
        let body = StartPayload(targetTemperature: targetTemperature)
        await performRequest(endpoint: "api/sauna/start", method: "POST", body: body) { _ in
            self.isHeating = true
        }
        await refreshStatus()
    }

    func stopSauna() async {
        await performRequest(endpoint: "api/sauna/stop", method: "POST") { _ in
            self.isHeating = false
        }
        await refreshStatus()
    }

    private func performRequest<T: Encodable>(
        endpoint: String,
        method: String = "GET",
        body: T? = nil,
        onSuccess: @escaping (Data) throws -> Void
    ) async {
        let baseURL = BridgeConfiguration.bridgeURL
        guard let url = URL(string: endpoint, relativeTo: baseURL) else {
            errorMessage = "Invalid bridge URL"
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if let body = body {
            request.httpBody = try? JSONEncoder().encode(body)
        }

        await execute(request: request, onSuccess: onSuccess)
    }

    private func execute(
        request: URLRequest,
        onSuccess: @escaping (Data) throws -> Void
    ) async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            let (data, response) = try await session.data(for: request)
            guard let httpResponse = response as? HTTPURLResponse else { throw SaunaError.invalidResponse }
            guard (200..<300).contains(httpResponse.statusCode) else { throw SaunaError.serverError(httpResponse.statusCode) }
            try onSuccess(data)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

enum SaunaError: LocalizedError {
    case invalidResponse
    case serverError(Int)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "The bridge returned an invalid response."
        case let .serverError(code):
            return "The bridge responded with status code \(code)."
        }
    }
}

private struct SaunaStatus: Decodable {
    let statusCode: Int
    let temperature: String
    let targetTemperature: String
}

private struct StartPayload: Encodable {
    let targetTemperature: Int
}

enum BridgeConfiguration {
    /// Update this value with the URL where the Flask bridge is hosted.
    static let bridgeURL = URL(string: "http://192.168.1.10:5000/")!
}
