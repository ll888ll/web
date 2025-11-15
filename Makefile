SHELL := /bin/bash

.PHONY: install enable test guard clean fmt bootstrap

install:
	sudo ops/cicf/install.sh

enable:
	sudo systemctl enable --now cicf-bridge.service cicf-capture.service cicf-watch.service cicf-dnsmon.service || true
	sudo systemctl enable --now dns-guard.service || true
	sudo systemctl enable --now cicf-clean.timer || true

test:
	sudo ops/cicf/selftest.sh || true

guard:
	sudo /usr/local/bin/dns-guard.sh

clean:
	rm -rf CICFlowMeter || true

fmt:
	shfmt -w ops/cicf/*.sh 2>/dev/null || true

bootstrap:
	sudo ops/cicf/auto-configure.sh || true
