# Dependency selection and updates

The public container baseline lives in
[images.lock.json](../../operations/validation/images.lock.json). Each record
contains its source tag, immutable manifest reference, observed Linux platforms
and resolution date. The manifest bytes were checked against the registry digest;
no image was pulled or runtime accepted during resolution. This is artifact
identity evidence, not a vulnerability review or publisher-signature attestation.
The [registry API](https://distribution.github.io/distribution/spec/api/) defines
these manifest/digest contracts.

## Updating container examples

1. Choose a deliberate upstream version and read its release/security notes.
2. Resolve/verify the manifest digest and target platform from the public registry.
3. Update the lock and all consuming env examples/Dockerfile together. Do not
   replace a digest with a mutable tag to get a trial past a failure.
4. Scan the images/dependencies and run the source/staging checks and isolated
   application trial. Record actual results; a new digest alone establishes none.
5. Review data/schema/API compatibility and recovery before promoting anywhere.

The demo API is built from pinned Python/psycopg inputs. It still requires its own
built artifact and review. A pinned base does not make build output bit-for-bit
reproducible; transitive build/runtime tooling, timestamps and platform must also
be controlled for that stronger claim. Host OS packages likewise are not frozen
into an immutable operating-system snapshot by this reference.

## Selecting the Docker package set for a new Ubuntu guest

Consult the [official Ubuntu installation procedure](https://docs.docker.com/engine/install/ubuntu/)
and the vendor's noble/amd64 package index from your separate preparation
workflow. Select compatible exact versions for engine, CLI, containerd, buildx
and Compose. Record the reviewed public signing-key checksum and chosen versions
in private operation inputs. Do not paste credentials into these files or use a
wildcard/version chosen merely because it is newest.

The role requests that complete selection as a single apt list, then reads package
facts and rejects any mismatch before starting services. The
[Ansible apt module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/apt_module.html)
supports lists of versioned packages. It does not promise an atomic, reversible
installation: a package failure can leave partial changes, so the operation still
needs a fresh-guest trial and a concrete recovery path. Never enable a downgrade
or remove a safeguard solely to force an update through.
