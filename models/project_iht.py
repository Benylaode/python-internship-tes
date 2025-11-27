# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json

class ProjectIHT(models.Model):
    _inherit = "project.project"
    _description = "Project IHT Enhancement"

    alamat = fields.Char(string="Alamat Lokasi Proyek")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")

    @api.model
    def get_coordinate_from_address(self, address):
        """Mengambil koordinat menggunakan geocoder bawaan Odoo."""
        if not address:
            return {"error": "Alamat kosong"}
        try:
            geo = self.env['base.geocoder'].geo_find(address)
        except KeyError:
            return {"error": "Service geocoder tidak tersedia"}

        if not geo or not isinstance(geo, list) or not geo[0]:
            return {"error": "Koordinat tidak ditemukan"}

        return {
            "lat": geo[0].get("latitude"),
            "lng": geo[0].get("longitude")
        }

    source_aplikasi_pendukung = fields.Char(
        string="Source Aplikasi Pendukung",
        help="URL aplikasi pendukung proyek"
    )

    daftar_pekerja_remote = fields.Text(
        string="Daftar Pekerja Remote (JSON)",
        help="Berisi JSON list pekerja remote"
    )

    @api.constrains('daftar_pekerja_remote')
    def _check_daftar_pekerja_remote_json(self):
        for record in self:
            if record.daftar_pekerja_remote:
                try:
                    json.loads(record.daftar_pekerja_remote)
                except json.JSONDecodeError:
                    raise ValidationError(
                        "Format JSON pada 'Daftar Pekerja Remote' tidak valid."
                    )