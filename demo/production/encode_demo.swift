import AppKit
import AVFoundation
import CoreVideo
import Foundation

let base = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let output = URL(fileURLWithPath: CommandLine.arguments[2])
try? FileManager.default.removeItem(at: output)

let width = 1280
let height = 720
let fps: Int32 = 15
let durations = [4, 5, 4, 7, 6, 5]
let writer = try AVAssetWriter(outputURL: output, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height,
    AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 3_000_000]
])
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input,
    sourcePixelBufferAttributes: [
        kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
        kCVPixelBufferWidthKey as String: width,
        kCVPixelBufferHeightKey as String: height,
    ])
guard writer.canAdd(input) else { fatalError("Cannot add video input") }
writer.add(input)
guard writer.startWriting() else { fatalError("Could not start writer: \(String(describing: writer.error))") }
writer.startSession(atSourceTime: .zero)

func makeBuffer(_ cgImage: CGImage) -> CVPixelBuffer {
    var buffer: CVPixelBuffer?
    let attrs = [kCVPixelBufferCGImageCompatibilityKey: true,
                 kCVPixelBufferCGBitmapContextCompatibilityKey: true] as CFDictionary
    let status = CVPixelBufferCreate(kCFAllocatorDefault, width, height,
                                     kCVPixelFormatType_32ARGB, attrs, &buffer)
    guard status == kCVReturnSuccess, let pixel = buffer else { fatalError("Pixel buffer error") }
    CVPixelBufferLockBaseAddress(pixel, [])
    let info = CGBitmapInfo.byteOrder32Big.rawValue | CGImageAlphaInfo.noneSkipFirst.rawValue
    guard let ctx = CGContext(data: CVPixelBufferGetBaseAddress(pixel), width: width,
                              height: height, bitsPerComponent: 8,
                              bytesPerRow: CVPixelBufferGetBytesPerRow(pixel),
                              space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: info) else {
        fatalError("Bitmap context error")
    }
    ctx.draw(cgImage, in: CGRect(x: 0, y: 0, width: width, height: height))
    CVPixelBufferUnlockBaseAddress(pixel, [])
    return pixel
}

var frame: Int64 = 0
for (index, duration) in durations.enumerated() {
    let path = base.appendingPathComponent(String(format: "slide-%02d.png", index + 1))
    guard let image = NSImage(contentsOf: path),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        fatalError("Could not read \(path.path)")
    }
    for _ in 0..<(duration * Int(fps)) {
        while !input.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.01) }
        guard adaptor.append(makeBuffer(cgImage),
                             withPresentationTime: CMTime(value: frame, timescale: fps)) else {
            fatalError("Could not append frame \(frame): \(String(describing: writer.error))")
        }
        frame += 1
    }
}
input.markAsFinished()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()
guard writer.status == .completed else { fatalError("Writer failed: \(String(describing: writer.error))") }
print("Created \(output.path): \(Double(frame) / Double(fps)) seconds, no audio")
