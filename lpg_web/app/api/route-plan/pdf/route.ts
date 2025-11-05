import { NextRequest } from 'next/server'
import PDFDocument from 'pdfkit'

export const runtime = 'nodejs'

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}))
  const { depot, orders = [], result } = body || {}

  const doc = new PDFDocument({ size: 'A4', margin: 40 })
  const chunks: Uint8Array[] = []
  return await new Promise<Response>((resolve) => {
    doc.on('data', (c: Uint8Array) => chunks.push(c))
    doc.on('end', () => {
      const totalLen = chunks.reduce((n, a) => n + a.length, 0)
      const pdf = new Uint8Array(totalLen)
      let offset = 0
      for (const c of chunks) { pdf.set(c, offset); offset += c.length }
      resolve(new Response(pdf, {
        status: 200,
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': 'attachment; filename="route-plan.pdf"',
        }
      }))
    })

    doc.fontSize(18).text('LPG Route Plan', { align: 'left' })
    doc.moveDown(0.5)
    const date = new Date().toLocaleString()
    doc.fontSize(10).fillColor('#555').text(`Generated: ${date}`)
    doc.moveDown(1)

    // Summary
    doc.fillColor('#000').fontSize(12).text('Summary', { underline: true })
    const totalKm = result?.total_distance_km ?? 0
    const totalMin = result?.total_time_min ?? 0
    doc.text(`Total Distance: ${totalKm.toFixed ? totalKm.toFixed(1) : totalKm} km`)
    doc.text(`Total Time: ${totalMin.toFixed ? totalMin.toFixed(0) : totalMin} min`)
    doc.moveDown(1)

    // Depot
    if (depot) {
      doc.fontSize(12).text('Depot', { underline: true })
      doc.fontSize(10).text(`Lat: ${depot[0]}  Lon: ${depot[1]}`)
      doc.moveDown(1)
    }

    // Orders
    doc.fontSize(12).text('Orders', { underline: true })
    doc.moveDown(0.5)
    doc.fontSize(10)
    orders.forEach((o: any) => {
      doc.text(`• #${o.id}  qty=${o.demand}  (${o.lat.toFixed?.(4)}, ${o.lon.toFixed?.(4)})  TW ${o.tw_start}-${o.tw_end}`)
    })

    // Routes (if present)
    if (result?.routes) {
      doc.moveDown(1)
      doc.fontSize(12).text('Routes', { underline: true })
      result.routes.forEach((r: number[], i: number) => {
        doc.fontSize(10).text(`Vehicle ${i + 1}: ${r.join(' → ')}`)
      })
    }

    doc.end()
  })
}
